---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

(classic-ui-images-label)=

# Image resolving and scaling

Image scaling is done in plone.namedfile.scaling and most interesting the ImageScaling view.

## Image tag

To get a HTML tag for an scaled image, you can use the ImageScaling view as follow:

```python
from plone import api

scale_util = api.content.get_view('images', context, request)
tag = scale_util.tag('leadimage', scale='mini')
```

or to get a specific size:

```python
from plone import api

scale_util = api.content.get_view('images', context, request)
tag = scale_util.tag('leadimage', width="600", height="200")
```

The first argument is the field name, followed by one of the following arguments:

	fieldname=None,
        scale=None,
        height=None,
        width=None,
        direction="thumbnail",


## Image scaling without tag creation

To just get the scaling infos, without creating a HTML tag, you can use the ImageScaling view as follow:

```python
from plone import api

scale_util = api.content.get_view('images', context, request)
image_scale = scale_util.scale('leadimage', scale='mini')
print(image_scale.url)  # http://localhost:8080/Plone/enl/@@images/3d182f34-8773-4f20-a79d-8774c3151b7e.jpeg
print(image_scale.width)  # 200
print(image_scale.height)  # 110
```

the most important properties:

- data
- fieldname
- height
- mimetype
- srcset
- srcset_attribute
- tag
- uid
- url
- width

You can get a tag from this point too:
```python
>>> print(image_scale.tag)

<img src="http://localhost:8080/Plone/news/newsitem1/@@images/9f676d46-0cb3-4512-a831-a5db4079bdfa.jpeg" alt="News Item 1!" title="News Item 1" height="21" width="32" srcset="http://localhost:8080/Plone/news/newsitem1/@@images/4a68513c-cffd-4de0-8a35-80627945b80f.jpeg 2x, http://localhost:8080/Plone/news/newsitem1/@@images/c32929c6-cb89-4ce7-846f-38adf29c09a4.jpeg 3x" />
```

or to get a specific size:

```python
from plone import api

scale_util = api.content.get_view('images', context, request)
tag = scale_util.scale('leadimage', width="600", height="200")
```

The first argument is the field name, followed by one of the following arguments:

	fieldname=None,
        scale=None,
        height=None,
        width=None,
        direction="thumbnail",

## Scaling direction / mode

The actual scaling is done in plone.scale:
In plone scale the `direction` argument is deprecated in favor of `mode` and values are converted as follow:

direction values | mode values
-----------------|------------
scale-crop-to-fit | contain
down | contain
scale-crop-to-fill | cover
up | cover
keep | scale
thumbnail | scale

For now plone.namedfile is still expecting the direction argument with the old values.

## Permissions

The ImageScaling view is checking explicitly the permissions the current user has, in case you want to access objects which are normally not accessible to the current user, you have to override the validate_access method in ImageScale. In Products.EasyNewsletter you can find an example of that.

