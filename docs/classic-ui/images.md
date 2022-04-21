---
html_meta:
  "description": "Image resolving and scaling in Plone Classic UI"
  "property=og:description": "Image resolving and scaling in Plone Classic UI"
  "property=og:title": "Image Handling"
  "keywords": "Plone, Classic UI, classic-ui, image, resize, scale"
---

(classic-ui-images-label)=

# Image handling

The default content types and behaviors use the field `plone.namedfile.NamedBlobImage` for all images.

For this field, image scaling and HTML tag creation is provided by the `plone.namedfile.scaling` module, specifically in the [`ImageScaling`](https://github.com/plone/plone.namedfile/blob/ecf33a2bc7a8c61888909bc383b3e08d80888e43/plone/namedfile/scaling.py#L350) view.

Given a Dexterity content type named `news-item1` with a `plone.namedfile.NamedBlobImage` field named `image`, we can use the following APIs to access the image scales and manage scales.

```{note}
We will use the image object as context in the following examples.
```

(classic-ui-images-default-scales-label)=

## Default scales

In `/@@imaging-controlpanel` Plone allows you to configure which scales are available and what dimensions they should have. By default we have the following scales configured:

* large 768:768
* preview 400:400
* mini 200:200
* thumb 128:128
* tile 64:64
* icon 32:32
* listing 16:16

You can add or change scales as you like.


(classic-ui-images-image-resolving-by-uri-label)=

## Image resolving by URI

Plone can resolve an image scale via URI in different ways.


(classic-ui-images-by-field-and-scale-name-label)=

### By field and scale name

Given our `news-item1` with the field `image`, we can get the name scale `thumb` as follows:

`http://localhost:8080/Plone/news-item1/@@images/image/thumb`

To get the original image, you can leave out the scale:

`http://localhost:8080/Plone/news-item1/@@images/image`


(classic-ui-images-by-cacheable-scale-uid-name-label)=

### By cacheable scale UID name

When an image scale is created, it will be cached under the name `UID.EXT` (i.e. `f4c34254b44ba351af7393bfe0296664.jpeg`) in the object annotations.
Scaling keeps the uploaded formats, except for TIFF which ends up as JPEG.
It can be resolved as follows:

`http://localhost:8080/Plone/news-item1/@@images/3d182f34-8773-4f20-a79d-8774c3151b7e.jpeg`

This is useful for caching URLs in Varnish or the browser.
In case the uploaded image or scale definitions have changed, they will be saved again under a different UID.
This changes the URL and forces either the browser, or a cache proxy such as Varnish, to fetch it again.
When a scale has changed, the old stored entry in the annotation will be deleted after 24 hours.
If one changes an image which is used in multiple pages, the updated versions will only be shown after a restart of the Plone instance, saving the pages again, or after 24 hours.


(classic-ui-images-image-tag-label)=

## Image tag

To get an HTML tag for a scaled image, you can use the `ImageScaling` view as follows:

```python
from plone import api

scale_util = api.content.get_view("images", context, request)
tag = scale_util.tag("image", scale="mini")
```

To get a specific image size:

```python
from plone import api

scale_util = api.content.get_view("images", context, request)
tag = scale_util.tag("image", width=600, height=200)
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

If you pass additional kwargs to `tag`, they become attributes on `tag`.


(classic-ui-images-image-scaling-no-tag-creation-label)=

## Image scaling without tag creation

To get the scaling information only without creating an HTML tag, you can use the `ImageScaling` view as follows:

```python
from plone import api

scale_util = api.content.get_view("images", context, request)
# The default `Image` content type's field name is "image".
# On the following line of code, "image" is the field name.
image_scale = scale_util.scale("image", scale="mini")
print(image_scale.url)
print(image_scale.width)
print(image_scale.height)
```

This will produce the following output:

```console
http://localhost:8080/Plone/news-item1/@@images/3d182f34-8773-4f20-a79d-8774c3151b7e.jpeg
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

Instead of using the configured named scales, you can get an HTML tag with any specific size in pixels:

```python
from plone import api

scale_util = api.content.get_view("images", context, request)
tag = scale_util.scale("image", width=600, height=200)
```

(classic-ui-images-using-image_scale0-in-templates-label)=

### Using image_scale in templates

You could use the URL-variant from above, but that would be an uncached version.
To create a cached scale in a page template you can do the following:

```xml
<div tal:define="scale_view context/@@images;
                 image_scale python: scale_view.scale('image', 'mini')">
  <img
    src="${python: image_scale.url}"
    width="${python: image_scale.width"
    height="${python: image_scale.height}"
    >
</div>
```

Or you can get the HTML tag back, and replace the current tag with it:

```xml
<div tal:define="scale_view context/@@images">
  <img tal:replace="structured python: scale_view.tag('image', 'mini')">
</div>
```

You can also provide the following keyword arguments to set `title`, `alt`, or `css_class` for the generated tag:

```xml
<div tal:define="scale_view context/@@images">
  <img tal:replace="structured python: scale_view.tag('banner', 'mini', title='The Banner', alt='Alternative text', css_class='banner')">
</div>
```

(classic-ui-images-get-image_scale-by-cached-uid-name-label)=

### Get image_scale by cached UID name

If you only have the cached image name from an URL and need to get the image scale, unfortunately you can't use restrictedTraverse(), as this will not be able to resolve the scale. But you can use this workaround, by calling the `publishTraverse` method in `ImageScaling` directly:

```python
import re
from plone import api

uri = "http://localhost:8080/Plone/news-item1/@@images/3d182f34-8773-4f20-a79d-8774c3151b7e.jpeg"
image_url = re.compile(r"(.*@@images)\/([a-zA-Z0-9.-]*)\/?([a-zA-Z]*)")

url_match = image_url.match(uri)
groups = url_match.groups()
# ("http://localhost:8080/Plone/news-item1", "3d182f34-8773-4f20-a79d-8774c3151b7e.jpeg")
scale_util = api.content.get_view("images", context, request)
image_scale = scaling_util.publishTraverse(context.REQUEST, groups[1])
```


(classic-ui-images-scaling-direction-label)=

## Scaling `direction`

The default direction is `thumbnail`.

Other options are:

* `down`
* `keep`
* `scale-crop-to-fill`
* `scale-crop-to-fit`
* `thumbnail`
* `up`


(classic-ui-images-permissions-label)=

## Permissions

The `ImageScaling` view explicitly checks the permissions of the current user.
To access image scales, which are normally not accessible to the current user, override the `validate_access` method in `plone.namedfile.scaling.ImageScale`.


## `srcset` configuration

In `/@@imaging-controlpanel` Plone allows you to define HTML `srcset` attributes.
A `srcset` can help the browser serve the best fitting image for the current users situation.
Which image scale is best for the user can be decided on different metrics.


### viewport size

The first is metric would be the viewport size.

```json
{
  "scale": "large",
  "media": "(max-width:800px)"
},
{
  "scale": "larger"
}
```

With this definition the Browser will use the large scale (800px) when the viewport size is max 800px.
When the viewport width is greater than 800 pixels, the browser will use the larger scale `1000px`.


### Pixel density

Another metric is the pixel density of the users screen.
This metric defines how many DPI per pixel the Screen is using.

```json
{
  "scale": "huge",
  "media": "(min-resolution: 192dpi), (-webkit-min-device-pixel-ratio: 2)"
},
{
  "scale": "large"
}
```

With this definition the browser will use the `huge` scale of 1600 pixels when the screen has a density of 192 DPI, also knows as `2x`.
We use here two different media queries to also support older Safari versions.
Mobile devices with Safari-like iPhones only support the old non-standard media query.
If you don't care about IE support you can also use `min-resolution: 2dppx` which is closer to `2x`.
The most common variants are:

- `1x`: 96 DPI
- `1.25x`: 120 DPI per pixel
- `1.5x`: 144 DPI per pixel
- `2x`: 192 DPI per pixel
- `3x`: 288 DPI per pixel


### Combining viewport size and pixel density

It is also possible to combine the two metrics.

```json
{
  "scale": "great",
  "media": "(max-width:799px) and (min-resolution: 144dpi), (max-width:799px) and (-webkit-min-device-pixel-ratio: 1.5)"
},
{
  "scale": "large",
  "media": "(max-width:799px)"
},
{
  "scale": "huge",
  "media": "(min-width:800px) and (min-resolution: 144dpi), (max-width:800px) and (-webkit-min-device-pixel-ratio: 1.5)"
},
{
  "scale": "larger",
  "media": "(min-width:800px)"
},
{
  "scale": "huge"
}
```
