---
myst:
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

In `/@@imaging-controlpanel` Plone allows you to configure which scales are available and what dimensions they should have.
By default, we have the following scales configured:

* huge 1600:65536
* great 1200:65536
* larger 1000:65536
* large 800:65536
* teaser 600:65536
* preview 400:65536
* mini 200:65536
* thumb 128:128
* tile 64:64
* icon 32:32
* listing 16:16

You can add or change scales as you like.
The scales are defined in `plone.base.interfaces.controlpanel`.


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

### By cacheable scale {term}`UID` name

When an image scale is created, it will be cached under the name `UID.EXT` (such as `f4c34254b44ba351af7393bfe0296664.jpeg`) in the object annotations.
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
    mode="scale"
)
```

If you pass additional `kwargs` to `tag`, they become attributes on `tag`.


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

(classic-ui-images-using-image_scale-in-templates-label)=

### Using `image_scale` in templates

You could use the URL-variant from above, but that version would not be cached.
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
  <img tal:replace="structure python: scale_view.tag('image', 'mini')">
</div>
```

You can also provide the following keyword arguments to set `title`, `alt`, or `css_class` for the generated tag:

```xml
<div tal:define="scale_view context/@@images">
  <img tal:replace="structure python: scale_view.tag('banner', 'mini', title='The Banner', alt='Alternative text', css_class='banner')">
</div>
```

(classic-ui-images-get-image_scale-by-cached-uid-name-label)=

### Get `image_scale` by cached {term}`UID` name

If you only have the cached image name from a URL and need to get the image scale, unfortunately you can't use `restrictedTraverse()`, as this will not be able to resolve the scale.
But you can use this workaround, by calling the `publishTraverse` method in `ImageScaling` directly:

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


(classic-ui-images-scaling-mode-label)=

## Scaling `mode`

```{versionchanged} 6.0
Added `mode` to replace the deprecated `direction`.
Added new option names for `mode` to align with CSS `background-size` values, and deprecated previous names `keep`, `thumbnail`, `scale-crop-to-fit`, `down`, `scale-crop-to-fill`, and `up`.
```

Scaling is intended for the optimal display of images in a web browser.

To scale an image, you can use the `mode` parameter to control the scaling output.
You must use either `width` or `height`, or both.

Three different scaling options are supported.
They correspond to the CSS [`background-size`](https://developer.mozilla.org/en-US/docs/Web/CSS/background-size) values.

The possible options for `mode` are listed below, where the default option is `scale`.

`scale`
:   This is the default option.
    `scale` scales to the requested dimensions without cropping.
    The resulting image may have a different size than requested.
    This option requires both `width` and `height` to be specified.
    It does not scale up.

    Deprecated option names: `keep`, `thumbnail`.

`contain`
:   `contain` starts by scaling the image either to the smaller dimension when you give both `width` and `height`, or to the only given dimension, then crops to the other dimension if needed.

    Deprecated option names: `scale-crop-to-fit`, `down`.

`cover`
:   `cover` scales the image either to the larger dimension when you give both `width` and `height`, or to the only given dimension, up to the size you specify.
    Despite the deprecated option name, it does not crop.

    Deprecated option names: `scale-crop-to-fill`, `up`.


(classic-ui-images-permissions-label)=

## Permissions

The `ImageScaling` view explicitly checks the permissions of the current user.
To access image scales, which are normally not accessible to the current user, override the `validate_access` method in `plone.namedfile.scaling.ImageScale`.


(classic-ui-images-responsive-image-support)=

## Responsive image support

Plone supports the generation of [`picture`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture) tags with `srcset`s for image optimization.
Additionally, you can define [media queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries) for [art direction](classic-ui-images-responsive-image-support-art-direction) and further optimization.

The configuration allows you to define different `picture` variants, such as `Large`, `Medium`, or `Small`.
Users can choose from them in editors, such as TinyMCE, and developers can use them in templates.

To generate a `picture` tag, use the following code.

```python
from plone import api

scale_util = api.content.get_view("images", context, request)
tag = scale_util.picture("image", scale="larger", picture_variant="large")
```

The same can be done from a template.

```xml
<div tal:define="scale_view context/@@images">
  <img tal:replace="structure python:scale_view.picture('image', scale='larger', picture_variant='large'" />
</div>
```

(classic-ui-images-responsive-image-support-picture-variants)=

### `picture` variants

In `/@@imaging-controlpanel` Plone allows you to define `picture` variants with a list of available image scales.
These are used for HTML {term}`srcset` attributes.
A `srcset` attribute can help the browser to serve the best fitting image size for the current user's display.


(classic-ui-images-responsive-image-support-default-configuration-label)=

### Default configuration

The default configuration covers image size optimization, and will provide the browser with the needed information to load the optimal image size.

```json
{
    "large": {
        "title": "Large",
        "sourceset": [
            "scale": "larger",
            "additionalScales": ["preview", "teaser", "large", "great", "huge"],
        ],
    },
    "medium": {
        "title": "Medium",
        "sourceset": [
            "scale": "teaser",
            "additionalScales": ["preview", "large", "larger", "great"],
        ],
    },
    "small": {
        "title": "Small",
        "sourceset": [
            "scale": "preview",
            "additionalScales": ["large", "larger"],
        ],
    },
}
```

### Optional settings

The `sourceset` property is an array and can have more than one entry.
If we have the following two entries, the `image_srcset` output filter will generate one `source` tag for each entry and an additional `img` tag from the last entry.

```json
{
    "medium": {
        "title": "Large",
        "sourceset": [
            {
              "scale": "mobile_crop",
              "media": "(max-width: 768px)",
              "additionalScales": ["mobile_crop_highres"],
            },
            {
             "scale": "teaser",
              "media": "(min-width: 769px)",
              "additionalScales": ["large", "larger", "great", "huge"],
            }
        ],
    },
}
```


(classic-ui-images-responsive-image-support-filtering-scales)=

#### Filtering scales

By default, for every `srcset`, all available scales will be included in the `srcset`.

```json
{
    "large": {
        "title": "Large",
        "sourceset": [
            {"scale": "larger"},
        ],
    },
}
```

To restrict the list of used scales inside a `srcset`, you can set the `additionalScales` parameter with an array of allowed scales.
Without this parameter, all scales which are not globally excluded scales will be used.

```json
    "small": {
        "title": "Small",
        "sourceset": [
            {
              "scale": "preview",
              "additionalScales": ["large", "larger", "great", "huge"],
            },
        ],
    },
```

This means the generated `srcset` will contain the scales from `preview` up to `huge`, but not `mini`, for example.


(classic-ui-images-responsive-image-support-picture-variant-in-editor)=

#### Hiding a `picture` variant in editors

It is possible to hide a `picture` variant in editors.
This is useful when you want to define a `picture` variant to be used in templates only.

```json
    "leadimage": {
        "title": "Lead image",
        "sourceset": [
            {
              "scale": "preview",
              "additionalScales": ["large", "larger"],
              "hideInEditor": true,
            },
        ],
    },
```


(classic-ui-images-responsive-image-support-art-direction)=

### Art direction

With image size optimization, the browser is able to choose the optimal image for each display size.
But we have no control over which scale the browser will actually use.
For example to force the browser to use a zoomed version of an image for smaller screens, we can use media queries.
The technique is called [art direction](https://developer.mozilla.org/en-US/docs/Web/HTML/Responsive_images#art_direction).

Let's have a look at a more advanced configuration:

```json
{
    "large": {
        "title": "Large",
        "sourceset": [
            {"scale": "larger"},
        ],
    },
    "medium": {
        "title": "Medium",
        "sourceset": [
            {
              "scale": "mobile_crop",
              "media": "(max-width: 768px)",
              "additionalScales": ["mobile_crop_highres"],
            },
            {
             "scale": "teaser",
              "media": "(min-width: 769px)",
              "additionalScales": ["large", "larger", "great", "huge"],
            }
        ],
    },
    "small": {
        "title": "Small",
        "sourceset": [
            {"scale": "preview"},
        ],
    },
}

```

This will result in a `srcset` as in the following example for a medium image:

```html
<picture>
  <source media="(max-width: 677px)"
          srcset="resolveuid/45fed06defa54d15b37c5b1dc882710c/@@images/image/mobile_crop 800w,
                  resolveuid/45fed06defa54d15b37c5b1dc882710c/@@images/image/mobile_crop_highres 1600w">
  <source media="(min-width: 678px)"
          srcset="resolveuid/45fed06defa54d15b37c5b1dc882710c/@@images/image/teaser 600w,
                  resolveuid/45fed06defa54d15b37c5b1dc882710c/@@images/image/large 800w,
                  resolveuid/45fed06defa54d15b37c5b1dc882710c/@@images/image/larger 1000w,
                  resolveuid/45fed06defa54d15b37c5b1dc882710c/@@images/image/great 1200w">
  <img alt="Alternative text"
       class="image-richtext image-size-medium"
       loading="lazy"
       src="resolveuid/45fed06defa54d15b37c5b1dc882710c/@@images/image/teaser"
       width="600"
       height="400">
</picture>
```

```{note}
Please note that this example has the `resolve_uid_and_caption` filter disabled to see the scale names better.
The real `src` URLs look more like `http://localhost:8080/Plone50/dsc04791.jpg/@@images/778f9c06-36b0-485d-ab80-12c623dc4bc3.jpeg`.
```

## Image scales from catalog brain

For all `NamedBlobImage` fields, we can get existing scale information directly from the catalog brain.

Given a content type with a `NamedBlobField` named `picture`, we can get the following information by calling the `image_scales` attribute on the catalog brain.

```python
(Pdb) pp brain.image_scales
{'picture': [{'content-type': 'image/jpeg',
              'download': '@@images/picture-800-ddae07fbc46b293155bd6fcda7f2572a.jpeg',
              'filename': 'my-picture.jpg',
              'height': 800,
              'scales': {'icon': {'download': '@@images/picture-32-f2f815374aa5434e06fb3a95306527fd.jpeg',
                                  'height': 32,
                                  'width': 32},
                         'large': {'download': '@@images/picture-800-4dab3b3cc42abb6fad29258c7430070a.jpeg',
                                   'height': 800,
                                   'width': 800},
                         'listing': {'download': '@@images/picture-16-d3ac2117158cf38d0e15c5f5feb8b75d.jpeg',
                                     'height': 16,
                                     'width': 16},
                         'mini': {'download': '@@images/picture-200-3de96ae4288dfb18f5589c89b861ecc1.jpeg',
                                  'height': 200,
                                  'width': 200},
                         'preview': {'download': '@@images/picture-400-60f60942c8e4ddd7dcdfa90527a8bae0.jpeg',
                                     'height': 400,
                                     'width': 400},
                         'teaser': {'download': '@@images/picture-600-1ada88b8af6748e9cbe18a34c3127443.jpeg',
                                    'height': 600,
                                    'width': 600},
                         'thumb': {'download': '@@images/picture-128-80fce253497f7a745315f58f3e8f3a0c.jpeg',
                                   'height': 128,
                                   'width': 128},
                         'tile': {'download': '@@images/picture-64-220d6703eac104c59774a379a8276e76.jpeg',
                                  'height': 64,
                                  'width': 64}},
              'size': 238977,
              'width': 800}]}
```

This information shows we have everything we need to generate our image URLs, without waking up any objects.

```xml
<li tal:define="preview python: brain.image_scales['picture'][0]['scales']['preview']">
  <img src="${brain/getURL}/${python: preview['download']}"
    width="${python: preview['width']}"
    height="${python: preview['height']}" />
</li>
```
