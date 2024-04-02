---
myst:
  html_meta:
    "description": "PLIP review"
    "property=og:description": "PLIP review"
    "property=og:title": "PLIP review"
    "keywords": "PLIP, review, Plone Improvement Proposal, Plone"
---

# PLIP review

A Plone Improvement Proposal (PLIP) is a formal process to propose a change to improve Plone.


## Expectations

A good PLIP review takes about four hours.
Please plan accordingly.
When you are done, if you have access to core, commit the review to the `plips` folder, and reference the PLIP in your commit message.
If you do not have access, attach your review to the PLIP ticket itself.


## Setting up the environment

Follow the instructions in {doc}`getting-started-with-development`.
You will need to checkout the branch to which the PLIP is assigned.
Instead of running the buildout with the default buildout file, you will run the configuration specific to that PLIP:

```shell
./bin/buildout -c plips/plipXXXX.cfg
```


## Functionality review

This section describes the topics that may be addressed in a PLIP review, depending on the nature of the PLIP itself.


### General

-   Does the PLIP actually do what the implementers proposed?
    Are there incomplete variations?
-   Were there any errors running buildout?
    Did the migration(s) work?
-   Do error and status messages make sense?
    Are they properly internationalized?
-   Are there any performance considerations?
    Has the implementer addressed them, if so?


### Bugs

-   Are there any bugs?
    Nothing is too big nor small.
-   Do fields handle wacky data?
    How about strings in date fields, or nulls in required?
-   Is validation up to snuff and sensical?
    Is it too restrictive or not restrictive enough?


### Usability Issues

-   Is the implementation usable?
-   How will novice end users respond to the change?
-   Does this PLIP need a usability review?
    If you think this PLIP needs a usability review, change the state to "please review" and add a note in the comments.
-   Is the PLIP consistent with the rest of Plone?
    For example, if there is control panel configuration, does the new form fit in with the rest of the panels?
-   Does everything flow nicely for novice and advanced users?
    Is there any workflow that feels odd?
-   Are there any new permissions and do they work properly?
    Does their role assignment make sense?


### Documentation Issues

- Is the corresponding documentation for the end user, be it developer or Plone user, sufficient?
- Is the change itself properly documented?

Report bugs or issues on GitHub as you would for any Plone bug.
Reference the PLIP in the bug, assign to its implementer, and add a tag for the PLIP in the form of `plip-xxx`.
This way the implementer can find help if they need it.
Also set a priority for the ticket.
The PLIP will not be merged until all blockers and critical bugs are fixed.


### Code Review


#### Python

-   Is this code maintainable?
-   Is the code properly documented?
-   Does the code adhere to PEP8 standards (more or less)?
-   Are they importing deprecated modules?


#### JavaScript

-   Does the JavaScript meet our set of JavaScript standards?
    See our section about [JavaScript](https://5.docs.plone.org/develop/addons/javascript/index.html) and the [JavaScript Style Guide](https://5.docs.plone.org/develop/styleguide/javascript.html).
-   Does the JavaScript work in all currently supported browsers?
    Is it performant?

```{todo}
Update links from Plone 5 Documentation to Plone 6 Documentation, when they exist.
See https://github.com/plone/documentation/issues/1330
```

#### ME/TAL

-   Does the PLIP use views appropriately, avoiding too much logic?
-   Is there any code in a loop that could potentially be a performance issue?
-   Are there any deprecated or old style ME/TAL lines of code, such as using `DateTime`?
-   Is the rendered HTML compliant with standards? Are IDs and classes used appropriately?
