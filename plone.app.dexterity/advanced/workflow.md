---
myst:
  html_meta:
    "description": "How to control security of content types with workflow in Plone"
    "property=og:description": "How to control security of content types with workflow in Plone"
    "property=og:title": "How to control security of content types with workflow in Plone"
    "keywords": "Plone, security, content types, workflow"
---

# Workflow

This chapter describes how to control security with workflow.

Workflow is used in Plone for three distinct, but overlapping purposes.

-   To keep track of metadata, chiefly an object's *state*.
-   To create content review cycles and model other types of processes.
-   To manage object security.

When writing content types, we will often create custom workflows to go with them.
In this section, we will explain at a high level how Plone's workflow system works, and then show an example of a simple workflow to go with our example types.
An exhaustive manual on using workflows is beyond the scope of this manual, but hopefully this will cover the basics.


## A DCWorkflow refresher

What follows is a fairly detailed description of [`DCWorkflow`](https://pypi.org/project/Products.DCWorkflow/).
You may find some of this a little detailed on first reading, so feel free to skip to the specifics later on.
However, it is useful to be familiar with the high level concepts.
You're unlikely to need multi-workflow chains in your first few attempts at workflow, for instance, but it's useful to know what it is if you come across the term.

Plone's workflow system is known as DCWorkflow.
It is a *states-and-transitions* system, which means that your workflow starts in a particular *state* (the *initial state*) and then moves to other states via *transitions* (also called *actions* in CMF).

When an object enters a particular state (including the initial state), the workflow is given a chance to update **permissions** on the object.
A workflow manages a number of permissions—typically the "core" CMF permissions
including {guilabel}`View`, {guilabel}`Modify portal content`, and so on—and will set those on the object at each state change.
Note that this is event-driven, rather than a real-time security check.
Only by changing the state is the security information updated.
This is why you need to click {guilabel}`Update security settings` at the bottom of the `portal_workflow` screen in the ZMI when you change your workflows' security settings and
want to update existing objects.

A state can also assign *local roles* to *groups*.
This is akin to assigning roles to groups on Plone's {guilabel}`Sharing` tab, but the mapping of roles to groups happens on each state change, much like the mapping of roles to permissions.
Thus, you can say that in the `pending_secondary` state, members of the {guilabel}`Secondary reviewers` group have the {guilabel}`Reviewer` local role.
This is powerful stuff when combined with the more usual role-to-permission mapping, although it is not very commonly used.

State changes result in a number of *variables* being recorded, such as the *actor* (the user that invoked the transition), the *action* (the name of the transition), the date and time, and so on.
The list of variables is dynamic, so each workflow can define any number of variables linked to [TALES](https://zope.readthedocs.io/en/latest/zopebook/AppendixC.html#tales-overview) expressions that are invoked to calculate the current value at the point of transition.
The workflow also keeps track of the current state of each object.
The state is exposed as a special type of workflow variable called the *state variable*.
Most workflows in Plone uses the name `review_state` as the state variable.

Workflow variables are recorded for each state change in the *workflow history*.
This allows you to see when a transition occurred, who effected it, and what state the object was in before or after.
In fact, the "current state" of the workflow is internally looked up as the most recent entry in the workflow history.

Workflow variables are also the basis for *worklists*.
These are basically pre-defined catalog queries run against the current set of workflow variables.
Plone's review portlet shows all current worklists from all installed workflows.
This can be a bit slow, but it does mean that you can use a single portlet to display an amalgamated list of all items on all worklists that apply to the current user.
Most Plone workflows have a single worklist that matches on the `review_state` variable, for example, showing all items in the `pending` state.

If states are the static entities in the workflow system, *transitions* (actions) provide the dynamic parts.
Each state defines zero or more possible exit transitions, and each transition defines exactly one target state, though it is possible to mark a transition as "stay in current state".
This can be useful if you want to do something in reaction to a transition and record that the transition happened in the workflow history, but not change the state (or security) of the object.

Transitions are controlled by one or more *guards*.
These can be permissions (the preferred approach), roles (mostly useful for the {guilabel}`Owner` role; in other cases it is normally better to use permissions) or TALES expressions.
A transition is available if all its guard conditions are true.
A transition with no guard conditions is available to everyone, including the anonymous user.

Transitions are user-triggered by default, but may be **automatic**.
An automatic transition triggers immediately following another transition, provided its guard conditions pass.
It will not necessarily trigger as soon as the guard condition becomes true, as that would involve continually re-evaluating guards for all active workflows on all objects.

When a transition is triggered, the `IBeforeTransitionEvent` and `IAfterTransitionEvent` **events**
are triggered.
These are low-level events from `Products.DCWorkflow` that can tell you a lot about the previous and current states.
There is a higher level `IActionSucceededEvent` in `Products.CMFCore` that is more commonly used to react after a workflow action has completed.

In addition to the events, you can configure workflow **scripts**.
These are either created through-the-web or (more commonly) as External Methods [^id2], and may be set to execute before a transition is complete, that is, before the object enters the target state, or just after it has been completed when the object is in the new state.
Note that if you are using event handlers, you'll need to check the event object to find out which transition was invoked, since the events are fired on all transitions.
The per-transition scripts are only called for the specific transitions for which they were configured.

[^id2]: An *External Method* is a Python script evaluated in Zope context.
    See [Logic Objects](https://zope.readthedocs.io/en/latest/zopebook/BasicObject.html#logic-objects-script-python-objects-and-external-methods) in the Zope 2 Book.


### Multi-chain workflows

Workflows are mapped to types via the `portal_workflow` tool.
There is a default workflow, indicated by the string `(Default)`.
Some types have no workflow, which means that they hold no state information and typically inherit permissions from their parent.
It is also possible for types to have *multiple workflows*.
You can list multiple workflows by separating their names by commas.
This is called a *workflow chain*.

Note that in Plone, the workflow chain of an object is looked up by multi-adapting the object and the workflow to the `IWorkflowChain` interface.
The adapter factory should return a tuple of string workflow names (`IWorkflowChain` is a specialization of `IReadSequence`, that is, a tuple).
The default obviously looks at the mappings in the `portal_workflow` tool, but it is possible to override the mapping, for example, by using a custom adapter registered for some marker interface, which in turn could be provided by a type-specific behavior.

Multiple workflows applied in a single chain co-exist in time.
Typically, you need each workflow in the chain to have a different state variable name.
The standard `portal_workflow` API (in particular, `doActionFor()`, which is used to change the state of an object) also assumes the transition IDs are unique.
If you have two workflows in the chain and both currently have a `submit` action available, only the first workflow will be transitioned if you do `portal_workflow.doActionFor(context, ‘submit')`.
Plone will show all available transitions from all workflows in the current object's chain in the `State` drop-down, so you do not need to create any custom user interface for this.
However, Plone always assumes the state variable is called `review_state` (which is also the variable indexed in `portal_catalog`).
Therefore, the state of a secondary workflow won't show up unless you build some custom UI.

In terms of security, remember that the role-to-permission (and group-to-local-role) mappings are event-driven and are set after each transition.
If you have two concurrent workflows that manage the same permissions, the settings from the last transition invoked will apply.
If they manage different permissions (or there is a partial overlap), then only the permissions managed by the most-recently-invoked workflow will change, leaving the settings for other permissions untouched.

Multiple workflows can be very useful in case you have concurrent processes.
For example, an object may be published, but require translation.
You can track the review state in the main workflow and the translation state in another.
If you index the state variable for the second workflow in the catalog (the state variable is always available on the indexable object wrapper, so you only need to add an index with the appropriate name to `portal_catalog`), you can search for all objects pending translation, for example, using a *Collection*.


## Creating a new workflow

With the theory out of the way, let's show how to create a new workflow.

Workflows are managed in the `portal_workflow` tool.
You can use the ZMI to create new workflows and assign them to types.
However, it is usually preferable to create an installable workflow configuration using GenericSetup.
By default, each workflow, as well as the workflow assignments, are imported and exported using an XML syntax.
This syntax is comprehensive, but rather verbose if you are writing it manually.

For the purposes of this manual, we will show an alternative configuration syntax based on spreadsheets (in CSV format).
This is provided by the [`collective.wtf`](https://pypi.org/project/collective.wtf/) package.
You can read more about the details of the syntax in its documentation.
Here, we will only show how to use it to create a simple workflow for the `Session` type, allowing members to submit sessions for review.

To use `collective.wtf`, we need to depend on it.
In {file}`setup.py`, we have the following.

```python
install_requires=[
    'collective.wtf',
],
```

```{note}
As before, the `<includeDependencies />` line in {file}`configure.zcml` takes care of configuring the package for us.
```

A workflow definition using `collective.wtf` consists of a CSV file in the `profiles/default/workflow_csv` directory, which we will create, and a {file}`workflows.xml` file in `profiles/default` which maps types to workflows.

The workflow mapping in {file}`profiles/default/workflows.xml` is shown below.

```xml
<?xml version="1.0"?>
<object name="portal_workflow">
    <bindings>
        <type type_id="example.conference.session">
            <bound-workflow workflow_id="example.conference.session_workflow"/>
        </type>
    </bindings>
</object>
```

The CSV file itself is found in {file}`profiles/default/workflow_csv/example.conference.session_workflow.csv`.
It contains the following, which was exported to CSV from an OpenOffice spreadsheet.
You can find the original spreadsheet with the [`example.conference` source code](https://github.com/collective/example.conference/tree/master/example/conference/profiles/default/workflow_csv).
This applies some useful formatting, which is obviously lost in the CSV version.

```{note}
For your own workflows, you may want to use [this template](https://github.com/collective/example.conference/blob/master/example/conference/profiles/default/workflow_csv/example.conference.session_workflow.ods) as a starting point.
```

```text
"[Workflow]"
"Id:","example.conference.session_workflow"
"Title:","Conference session workflow"
"Description:","Allows members to submit session proposals for review"
"Initial state:","draft"

"[State]"
"Id:","draft"
"Title:","Draft"
"Description:","The proposal is being drafted."
"Transitions","submit"
"Permissions","Acquire","Anonymous","Authenticated","Member","Manager","Owner","Editor","Reader","Contributor","Reviewer"
"View","N",,,,"X","X","X","X",,
"Access contents information","N",,,,"X","X","X","X",,
"Modify portal content","N",,,,"X","X","X",,,


"[State]"
"Id:","pending"
"Title:","Pending"
"Description:","The proposal is pending review"
"Worklist:","Pending review"
"Worklist label:","Conference sessions pending review"
"Worklist guard permission:","Review portal content"
"Transitions:","reject, publish"
"Permissions","Acquire","Anonymous","Authenticated","Member","Manager","Owner","Editor","Reader","Contributor","Reviewer"
"View","N",,,,"X","X","X","X",,"X"
"Access contents information","N",,,,"X","X","X","X",,"X"
"Modify portal content","N",,,,"X","X","X",,,"X"

"[State]"
"Id:","published"
"Title:","Published"
"Description:","The proposal has been accepted"
"Transitions:","reject"
"Permissions","Acquire","Anonymous","Authenticated","Member","Manager","Owner","Editor","Reader","Contributor","Reviewer"
"View","Y","X",,,,,,,,
"Access contents information","Y","X",,,,,,,,
"Modify portal content","Y",,,,"X","X","X",,,

"[Transition]"
"Id:","submit"
"Title:","Submit"
"Description:","Submit the session for review"
"Target state:","pending"
"Guard permission:","Request review"

"[Transition]"
"Id:","reject"
"Title:","Reject"
"Description:","Reject the session from the program"
"Target state:","draft"
"Guard permission:","Review portal content"

"[Transition]"
"Id:","publish"
"Title:","Publish"
"Description:","Accept and publish the session proposal"
"Target state:","published"
"Guard permission:","Review portal content"
```

Here, you can see several states and transitions.
Each state contains a role/permission map, and a list of the possible exit transitions.
Each transition contains a target state and other meta-data, such as a title and a description, as well as guard permissions.

```{note}
Like most other GenericSetup import steps, the workflow uses the Zope 2 permission title when referring to permissions.
```

When the package is (re-)installed, this workflow should be available under `portal_workflow` and mapped to the `Session` type.

```{note}
If you have existing instances, don't forget to go to `portal_workflow` in the ZMI and click {guilabel}`Update security settings` at the bottom of the page.
This ensures that existing objects reflect the most recent security settings in the workflow.
```

## A note about add permissions

This workflow assumes that regular members can add *Session* proposals to *Programs*, which are then reviewed.
Previously, we granted the `example.conference: Add session` permission to the `Member` role.
This is necessary, but not sufficient to allow members to add sessions to programs.
The user will also need the generic `Add portal content` permission in the `Program` folder.

There are two ways to achieve this:

-   Build a workflow for the `Program` type that manages this permission.
-   Use the {guilabel}`Sharing` tab to grant {guilabel}`Can add` to the {guilabel}`Authenticated Users` group.
    This grants the {guilabel}`Contributor` local role to members.
    By default, this role is granted the {guilabel}`Add portal content` permission.
