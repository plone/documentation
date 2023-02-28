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

In Plone, a portlet is a small, modular visual element that can be added to a specific area of a web page, such as the right or left columns, or the footer.
Portlets can be used to display a variety of information, such as the latest news, upcoming events, or a list of related documents.
They can also be prepared to store their own set of fields, allowing users to add custom content to the portlet.
Portlets are typically used to provide relevant information to users in the context of the current page, hierarchy, user, or group.

Inheritance of Plone portlets allows for the automatic display of portlets in child items within the content hierarchy.
This means that if a portlet is set on a parent folder, all child items within that folder will automatically display the portlet unless it is explicitly blocked.
This can be useful for displaying consistent information throughout a section of the website, without having to individually set the portlet on each child item.
The inheritance of portlets can be overridden at any level of the content hierarchy, allowing for fine-grained control over the display of portlets on the website.

Portlets are highly customizable and can be used to display a wide variety of information.
They can be added, removed, or rearranged on a web page by users with the appropriate permissions, allowing for a high degree of flexibility in the layout and content of a Plone site.

Plone comes with several built-in portlets, such as the news portlet, the events portlet, and the login portlet.
In addition, developers can create custom portlets to display specific types of information or to provide specific functionality.

## Adding a portlet to a page

As a user, you can add a portlet to a web page in a Plone site by following these steps:

1. Navigate to the web page where you want to add the portlet.

2. Click on the {guilabel}`Manage portlets` link in the toolbar of the page and select the region on the page to modify.
   This will open the screen to manage portlets for the current item.

   Note that you must have the appropriate permissions to add portlets to a web page.
   If you do not see the {guilabel}`Manage portlets` link, you may need to contact the site administrator to request access.

3. In the {menuselection}`Add portlets` menu, select the portlet type that you want to add, and click the {guilabel}`Add` button.
  This will open a form to edit the settings for the selected portlet type.

4. Click the {guilabel}`Save` button to save your changes and add the portlet to the web page.
   This adds the portlet to the list of {guilabel}`Portlets assigned here` on the screen.

5. Use the {guilabel}`Up` and {guilabel}`Down` arrows in the {guilabel}`Assigned portlets` section to change the order in which the portlets will be displayed on the web page.
   The {guilabel}`Hide` button will deactivate the portlet.
   The {guilabel}`X` button deletes the portlet.
   These options will only appear at the root from which the object inherits its settings.


## Writing a custom Portlet

To create a portlet, you will need to write Python classes that define the portlet and its behavior.
This class should subclass the `Portlet` class from the `plone.portlets` package.

Here is an example of a very simple portlet class `my_portlet.py`:

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
        "manage portlets" screen. Here we use the message as a part of the title.
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

Here is the example for a simple page template `my_portlet.pt`:

```html
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

To register this portlet with Plone, you will need to create a `configure.zcml` file that tells Plone about the portlet.
After a restart, you can add it to a Plone page using the {guilabel}`Manage portlets` screen.
Here is an example `configure.zcml` file that registers the `MyPortlet` class defined above:

```xml
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

Title
: `Example Portlet`

Description
: `A portlet that displays a greeting message`

Add form
: `example.portlet.add`

Edit form
: `example.portlet.edit`

Assignment
: `example.portlet.Assignment`

Renderer
: `example.portlet.Renderer`

Schema
: `example.portlet.IExamplePortlet`

These values should match the corresponding classes and interfaces defined in the example code from the previous example.

This file registers the `MyPortlet` class as a portlet with Plone. It also specifies the portlet's name, title, description, and category.

For more examples of how to write and register portlets, look at the source code of the Plone core package [`plone.app.portlets`](https://github.com/plone/plone.app.portlets), or of other Plone add-ons that include portlets.
