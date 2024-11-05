---
myst:
  html_meta:
    "description": "Creating content types to manage tasks in Plone."
    "property=og:description": "Creating content types to manage tasks in Plone."
    "property=og:title": "Creating content types to manage tasks in Plone."
    "keywords": "Content Types, FTI, Dexterity, plonecli, bobtemplates.plone"
---

# Creating content types

When we attempt to solve a particular content management problem with Plone, we will often design new content types.
For the purpose of this example, we'll build a simple set of types to manage tasks.

-   We will use a content type `Tasks` to hold all task objects and present a list of tasks to the user.
    This type is folderish (`Container`).
-   We will use a content type `Task` with the information about the task.
    Fields include name, description, and status of the task.
    This type is non-folderish (`Item`).

## Creating a Plone package

We typically create a content type inside a Plone package.
We will use the {term}`plonecli` to create a Plone package and our content types.

```shell
plonecli create addon collective.tasks
cd collective.tasks
```

## Adding content types

Let's add a content type called `Tasks`:

```shell
plonecli add content_type
```

Fill in the name `Tasks` for the first content type:

```console
-> Content type name (Allowed: _ a-z A-Z and whitespace) [Todo Task]: Tasks
```

We keep the default base class `Container` here:

```console
--> Dexterity base class (Container/Item) [Container]:
```

We keep the default `globally addable`:

```console
--> Should the content type globally addable? [y]:
```

We want to filter content types, which can be added to this container:

```console
--> Should we filter content types to be added to this container? [n]: y
```

We keep the default behaviors active:

```console
--> Activate default behaviors? [y]:
```

Now let's add a content type called `Task`:

```shell
plonecli add content_type
```

Fill in the name `Task` for the first content type:

```console
-> Content type name (Allowed: _ a-z A-Z and whitespace) [Todo Task]: Task
```

We change the base class to `Item` here:

```console
--> Dexterity base class (Container/Item) [Container]: Item
```

We don't want it to be globally addable `globally addable`:

```console
--> Should the content type globally addable? [y]: n
```

If we disable `globally addable`, the next question will ask for the parent content type, where we will answer `Tasks`:

```console
--> Parent container portal_type name: Tasks
```

For the rest of the questions, we can keep the defaults.

To test our new Plone package and its content types, we can use {term}`plonecli` to build a development environment and start Plone.

```shell
plonecli build
plonecli serve
```

Your Plone is now running on http://localhost:8080.
You can add a new Plone site, enable your add-on, and add your content types.

```{seealso}
{term}`plonecli` takes care of all the details of a content type and its configuration.
For more configuration details, see {doc}`fti`.
```

For now your content type doesn't have any custom schema with fields defined.

See {doc}`/backend/schemas`, {doc}`/backend/fields` and {doc}`/backend/widgets` for information on how to add custom fields and widgets to your content type.

Also have a look at Plone {doc}`/backend/behaviors`, which provide default features you can enable per content type.
