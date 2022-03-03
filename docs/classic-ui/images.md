---
html_meta:
  "description": "Image resolution and scaling in Plone Classic UI"
  "property=og:description": "Image resolution and scaling in Plone Classic UI"
  "property=og:title": "Image resolving and scaling"
  "keywords": "Plone, Classic UI, classic-ui, image, resize, scale"
---

(classic-ui-images-label)=

# Image resolving and scaling

Image scaling is done in `plone.namedfile.scaling`, specifically in the `ImageScaling` view.


(classic-ui-images-image-tag-label)=

## Image tag

To get an HTML tag for a scaled image, you can use the `ImageScaling` view as follows:

```python
from plone import api

scale_util = api.content.get_view("images", context, request)
tag = scale_util.tag("leadimage", scale="mini")
```

To get a specific image size:

```python
from plone import api

scale_util = api.content.get_view("images", context, request)
tag = scale_util.tag("leadimage", width="600", height="200")
```

The complete list of arguments with their default values is shown in the following example.

```python
from plone import api

scale_util = api.content.get_view("images", context, request)
tag = scale_util.tag(
    fieldname=None,
    scale=None,
    height=None,
    width=None,
    direction="thumbnail"
)
```


(classic-ui-images-image-scaling-no-tag-creation-label)=

## Image scaling without tag creation

To get the scaling information only without creating an HTML tag, you can use the `ImageScaling` view as follows:

```python
from plone import api

scale_util = api.content.get_view("images", context, request)
# on the following line "leadimage" is the field name. The default Image content types field name is "image".
image_scale = scale_util.scale("leadimage", scale="mini")
print(image_scale.url)
print(image_scale.width)
print(image_scale.height)
```

This will produce the following output:

```console
http://localhost:8080/Plone/enl/@@images/3d182f34-8773-4f20-a79d-8774c3151b7e.jpeg
200
110
```

The most important properties are the following:

-   `data`
-   `fieldname`
-   `height`
-   `mimetype`
-   `srcset`
-   `srcset_attribute`
-   `tag`
-   `uid`
-   `url`
-   `width`

You can directly create an HTML tag from `image_scale`:

```pycon
>>> print(image_scale.tag())

<img src="http://localhost:8080/Plone/news/newsitem1/@@images/9f676d46-0cb3-4512-a831-a5db4079bdfa.jpeg" alt="News Item 1!" title="News Item 1" height="21" width="32" srcset="http://localhost:8080/Plone/news/newsitem1/@@images/4a68513c-cffd-4de0-8a35-80627945b80f.jpeg 2x, http://localhost:8080/Plone/news/newsitem1/@@images/c32929c6-cb89-4ce7-846f-38adf29c09a4.jpeg 3x" />
```

Instead of using the configured named scales you can also get an HTML tag with any specific size in pixels:

```python
from plone import api

scale_util = api.content.get_view("images", context, request)
tag = scale_util.scale("leadimage", width="600", height="200")
```


(classic-ui-images-scaling-direction-deprecated-in-favor-of-label)=

## Scaling `direction` deprecated in favor of `mode`

The actual scaling is done in `plone.scale`.
In Plone 6 in `plone.scale`, the `direction` argument is deprecated in favor of `mode`.
The values should be converted as follows:

direction values | mode values
-----------------|------------
scale-crop-to-fit | contain
down | contain
scale-crop-to-fill | cover
up | cover
keep | scale
thumbnail | scale

For now `plone.namedfile` still expects the `direction` argument with the old values.


(classic-ui-images-permissions-label)=

## Permissions

The `ImageScaling` view explicitly checks the permissions of the current user.
To access image scales which are normally not accessible to the current user override the `validate_access` method in `plone.namedfile.scaling.ImageScale`.
In `Products.EasyNewsletter` you can find an example of that.
