---
myst:
  html_meta:
    "description": "Creating content types to manage tasks."
    "property=og:description": "Creating content ttypes to manage tasks."
    "property=og:title": "Creating content types"
    "keywords": "Content Types, FTI, Dexterity, plonecli, bobtemplates.plone"
---

# Creating content types

When we attempt to solve a particular content management problem with Plone, we will often design new content types.
For the purpose of this example, we'll build a simple set of types to manage tasks.

- A content type `Tasks` is used to hold all task objects and present a list of tasks to the user.
  This type is folderish (Container).
- A content type `Task` with the information about the task.
  Fields include name, description, and status of the task.
  This type is non-folderish (Item).

## Creating a Plone package

A content type is typically created inside a Plone package. We will use the {term}`plonecli` to create a Plone package and our content types.

```sh
$ plonecli create addon collective.tasks
cd collective.tasks
```

## Adding content types

Let's add a content type called `Tasks`:

```sh
$ plonecli add content_type
```

fill in the name `Tasks` for the first content type:

```sh
-> Content type name (Allowed: _ a-z A-Z and whitespace) [Todo Task]: Tasks
```

we keep the default base class `Container` here:

```sh
--> Dexterity base class (Container/Item) [Container]:
```

we keep the default `globally addable`:

```sh
--> Should the content type globally addable? [y]:
```

we want to filter content types, which can be added to this container:

```sh
--> Should we filter content types to be added to this container? [n]: y
```

we keep the default behaviors active:

```sh
--> Activate default behaviors? [y]:
```

now let's add a content type called `Task`:

```sh
$ plonecli add content_type
```

fill in the name `Task` for the first content type:

```sh
-> Content type name (Allowed: _ a-z A-Z and whitespace) [Todo Task]: Task
```

we change the base class to `Item` here:

```sh
--> Dexterity base class (Container/Item) [Container]: Item
```

we don't want it to be globally addable `globally addable`:

```sh
--> Should the content type globally addable? [y]: n
```

if we disable globally addable, we will be ask a new question, for the parent content type, where we will answer `Tasks`:

```sh
--> Parent container portal_type name: Tasks
```

for the rest of the question we can keep the defaults.

To test our new Plone package and it's content types, we can use {term}`plonecli` to build a development environment and start Plone.

```sh
$ plonecli build
$ plonecli serve
```

Your Plone is now running on http://localhost:8080. You can add a new Plone site, enable your addon and add your content types.

```{note}
{term}`plonecli` takes care of all the details of a content type and it's configuration, for more configuration details see {ref}`backend-content-types-fti-label`.
```

For now your content type don't have any custom schema with fields defined.

See {ref}`backend-schemas-label`, {ref}`backend-fields-label` and {ref}`backend-widgets-label` for information on how to add custom fields and widgets to your content type.

Also have a look at Plone {ref}`backend-behaviors-label`, which provide default features you can enable on per content type basis.