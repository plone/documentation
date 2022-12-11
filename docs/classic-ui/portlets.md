---
myst:
  html_meta:
    "description": "Basic information about portlets in classic UI"
    "property=og:description": "Basic information about portlets in classic UI"
    "property=og:title": "Portlets"
    "keywords": "portlets"
---

(classic-ui-portlets-label)=

# Portlets

## What is a Portlet?

In Plone, a portlet is a small, modular piece of content that can be displayed in a specific area of a web page. Portlets are typically used to display information that is relevant to the current context, such as the latest news, upcoming events, or a list of related documents.

The context is either the current part of the content hierarchy, the current user's group memberships, or the current content type.
Thus, if a portlet was set on a folder, all contained items do display the portlet unless it is explicitly blocked.

Portlets are highly customizable and can be used to display a wide variety of information.
They can be added, removed, or rearranged on a web page by users with the appropriate permissions, allowing for a high degree of flexibility in the layout and content of a Plone site.

Plone comes with several built-in portlets, such as the news portlet, the events portlet, and the login portlet.
In addition, developers can create custom portlets to display specific types of information or to provide specific functionality.

## Adding a portlet to a page

As a user, you can add a portlet to a web page in a Plone site by following these steps:

1. Navigate to the web page where you want to add the portlet.

2. Click on the "Manage portlets" link in the toolbar of the page and select the region on the page to modify.
   This will open the "Manage portlets" screen.

3. In the "Add portlets" menu, select the portlet that you want to add and click the "Add" button.
  This will open an edit form, now fill in the form.

4. Click the "Save" button to save your changes and add the portlet to the web page.
   This adds the portlet to the list of "Portlets assigned here" on the screen.
   Note that you must have the appropriate permissions to add portlets to a web page.
   If you do not see the "Manage portlets" link, you may need to contact the site administrator to request access.

5. Use the "Up" and "Down" arrows in the "Assigned portlets" section to change the order in which the portlets will be displayed on the web page.
   The "Hide" button will deactivate the portlet.
   The "X" button deletes the portlet.


## Writing a custom Portlet

To create a portlet, you will need to write Python classes that define the portlet and its behavior.
This class should subclass the Portlet class from the `plone.portlets` package.

Here is an example of a very simple portlet class ``my_portlet.py``:

```python
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class IExamplePortlet(IPortletDataProvider):
    """A portlet that displays a greeting message."""

    message = schema.TextLine(
        title="Greeting message",
        description="The message to display in the portlet.",
        required=True,
    )


@implementer(IExamplePortlet)
class Assignment(base.Assignment):
    """Portlet assignment."""

    def __init__(self, message="Hello World!"):
        self.message = message

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Heres, we use the message as a part of the title.
        """
        return f"Greeting: {self.message}"


class Renderer(base.Renderer):
    """Portlet renderer."""

    # Define the page template that will be used to render the portlet
    template = ViewPageTemplateFile("my_portlet.pt")

    def message(self):
        """This method is called by the page template to render the portlet."""
        return self.data.message

    def render(self):
        """This method is called whenever the portlet is rendered."""
        return self.template()


class AddForm(base.AddForm):
    """Portlet add form."""

    schema = IExamplePortlet
    label = "Add Greeting Portlet"
    description = "This portlet displays a greeting."

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form."""

    schema = IExamplePortlet
    label = "Edit Greeting Portlet"
    description = "This portlet displays a greeting."

```

Here is the example for a simple page template ``my_portlet.pt``:

```HTML
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal"
  xmlns:i18n="http://xml.zope.org/namespaces/i18n"
  tal:omit-tag=""
>
  <div class="card portlet" i18n:domain="my-example">
    <div class="card-header">Greeter</div>

    <div class="card-body">
      <p>${python:view.message()}</p>
    </div>

    <div class="card-footer portletFooter"></div>
  </div>
</html>
```

This portlet class defines a portlet with the title "My Portlet" and the name "my-portlet". When the portlet is rendered, it will use the template file `my_portlet.pt` to generate its HTML output that displays a greeting message.

The message is set when the portlet is added and can be edited in the portlet's edit form.

To register this portlet with Plone, you will need to create a ``configure.zcml`` file that tells Plone about the portlet, and - after a restart - you can add it to a Plone page using the "manage portlets" screen.
Here is an example ``configure.zcml`` file that registers the MyPortlet class defined above:

```XML
<configure xmlns="http://namespaces.zope.org/zope"
           xmlns:browser="http://namespaces.zope.org/browser"
           xmlns:plone="http://namespaces.plone.org/plone"
           i18n_domain="example.portlet">

  <plone:portlet
      title="Example Portlet"
      description="A portlet that displays a greeting message"
      addview="example.portlet.add"
      editview="example.portlet.edit"
      assignment="example.portlet.Assignment"
      renderer="example.portlet.Renderer"
      schema="example.portlet.IExamplePortlet"
  />

</configure>
```

This file registers a portlet with the following properties:

- *Title:* Example" Portlet"
- *Description:* "A portlet that displays a greeting message"
- *Add form:* "example.portlet.add"
- *Edit form:* "example.portlet.edit"
- *Assignment:* "example.portlet.Assignment"
- *Renderer:* "example.portlet.Renderer"
- *Schema:* "example.portlet.IExamplePortlet"

These values should match the corresponding classes and interfaces defined in the example code from the previous answer.

This file registers the MyPortlet class as a portlet with Plone. It also specifies the portlet's name, title, description, and category.

To get more examples you can also look at the source code of the Plone core package (plone.app.portlets)[https://github.com/plone/plone.app.portlets], or of other Plone add-ons that include portlets for examples of how to write and register portlets.
