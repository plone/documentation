---
myst:
  html_meta:
    "description": "MyST syntax reference with examples"
    "property=og:description": "MyST syntax reference with examples"
    "property=og:title": "MyST syntax reference with examples"
    "keywords": "Documentation, Plone, Sphinx, MyST, reStructuredText, Markdown, syntax, examples"
---

(contributing-myst-reference)=

# MyST reference

This chapter provides information and examples for how to write proper MyST syntax—with references to Sphinx extensions for their specific directives—in Plone Documentation.


## MyST, reStructuredText, and Markdown

We use [MyST, or Markedly Structured Text](https://myst-parser.readthedocs.io/en/latest/), a rich and extensible flavor of Markdown, for authoring training documentation.

MyST extends {term}`Markdown` by incorporating all the features of {term}`reStructuredText` and {term}`Sphinx` and its extensions.
Contributors are welcome to use either Markdown or MyST syntax.

MyST may be more familiar to reStructuredText authors.
MyST allows the use of a {term}`fence` and `{rst-eval}` to evaluate native reStructuredText.
This may be useful when Markdown does not provide sufficient flexibility, such as for `figure`.


## MyST syntax reference

The following are frequently used snippets and examples.

```{seealso}

Official MyST documentation

- [The MyST Syntax Guide](https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html)
- [MyST Syntax Reference](https://myst-parser.readthedocs.io/en/latest/syntax/reference.html)
```


### Cross-references

```{seealso}
[The MyST Syntax Guide > Cross-references](https://myst-parser.readthedocs.io/en/latest/syntax/cross-referencing.html)
```

#### Link to a chapter or page

```md
Here is how to set up and build the documentation locally {doc}`/contributing/setup-build`.
```

Here is how to set up and build the documentation locally {doc}`/contributing/setup-build`.


(myst-reference-link-heading-label)=

#### Link to a heading

```md
(myst-reference-hello-heading-label)=

##### Hello heading

Read the section {ref}`myst-reference-link-heading-label`.
```

(myst-reference-hello-heading-label)=

##### Hello heading

Read the section {ref}`myst-reference-hello-heading-label`.


#### Link to an arbitrary location

```md
(example-target-label)=

I have an HTML anchor above me.

Click the link to visit {ref}`my text <example-target-label>`.
```

(example-target-label)=

I have an HTML anchor above me.

Click the link to visit {ref}`my text <example-target-label>`.


#### Link to external page

```md
Use [Shimmer](http://example.com) for cleaner whiter teeth.
```

Use [Shimmer](http://example.com) for cleaner whiter teeth.


### Images and figures

[Figures](https://docutils.sourceforge.io/docs/ref/rst/directives.html#figure) allow a caption and legend, whereas [images](https://docutils.sourceforge.io/docs/ref/rst/directives.html#images) do not.
However we can {ref}`enhance images with cards <enhance-images-label>` to add a caption and more features.

Use `image` for anything but diagrams.

Use `figure` for diagrams.


(static-assets-label)=

#### Static assets

When the documentation is in a submodule, paths to static assets—including, images, figures, and videos—must resolve in both the main documentation and the submodule's documentation.

Inside the `docs` directory, place static assets in the `/_static/` directory, and preferably inside a subdirectory named after the part or page of the documentation.
For example, in the `volto` submodule, inside its `src/docs` directory, place an image at `/_static/user-manual/block-left-add-icon.png`.
In your markup, use that same `docs`-root-relative path for the target, such as `/_static/user-manual/block-left-add-icon.png`.
Don't use file-relative paths.

Configuration in the `conf.py` files for the main documentation and its submodules handle the resolution of `docs`-root-relative paths for you.


#### Width of media

The main content area of a page in the documentation is 743 pixels wide.
When taking screenshots or videos, resize your browser window, or try to limit the width of your media to 740 pixels.
This will preserve legibility of images.


(enhance-images-label)=

#### Enhance images

We use cards from the Sphinx extension [`sphinx-design`](https://sphinx-design.readthedocs.io/en/latest/cards.html) to enhance the display and functionality of images.

Cards allow the display of a caption, create a link to the source image to display when it is too large to fit within the documentation page without scaling, and add a border to demarcate the image from the page's white background.

The following MyST example will display as shown below.

`````md
````{card}
```{image} /_static/caching/caching-disabled.png
:alt: Caching Control Panel
:target: /_static/caching/caching-disabled.png
```
+++
_Caching Control Panel_
````
`````

````{card}
```{image} /_static/caching/caching-disabled.png
:alt: Caching Control Panel
:target: /_static/caching/caching-disabled.png
```
+++
_Caching Control Panel_
````


#### Accessibility with `alt` text

From [Web Accessibility In Mind (WebAIM)](https://webaim.org/techniques/alttext/):

> Alternative text serves several functions:
> - It is read by screen readers in place of images allowing the content and function of the image to be accessible to those with visual or certain cognitive disabilities.
> - It is displayed in place of the image in browsers if the image file is not loaded or when the user has chosen not to view images.
> - It provides a semantic meaning and description to images which can be read by search engines or be used to later determine the content of the image from page context alone.

Accessibility is part of the [Plone brand and identity](https://plone.org/accessibility).

The following MyST example will display as shown below.

````md
```{image} /_static/standards.png
:alt: XKCD "Standards" comic strip
```
````

```{image} /_static/standards.png
:alt: XKCD "Standards" comic strip
```


#### Inline images

For inline images, we use the MyST extension [`html_image`](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#html-images).
Example syntax is shown below.

```html
You can copy <img alt="Copy icon" src="../../_images/copy.svg" class="inline"> blocks.
```

Note that the HTML attribute `class` must be set to `inline` to render the image inline at `1rem`. 

The above syntax renders as shown below.

> You can copy <img alt="Copy icon" src="/_static/copy.svg" class="inline"> blocks.

Images and figures should always include `alt` text.

The following MyST example will display as shown below.

````md
```{eval-rst}
.. figure:: /_static/voting_flowchart.png
    :alt: Voting flowchart

    This is a caption in a single paragraph.
    
    This is a legend, which consists of all elements after the caption.
    It can include a table.
    
    ======  =======
    Symbol  Meaning
    ======  =======
    ⃞       Object
    ⬭       View
    ➞       Flow
    ======  =======
```
````

```{eval-rst}
.. figure:: /_static/voting_flowchart.png
    :alt: Voting flowchart

    This is a caption in a single paragraph.
    
    This is a legend, which consists of all elements after the caption.
    It can include a table.
    
    ======  =======
    Symbol  Meaning
    ======  =======
    ⃞       Object
    ⬭       View
    ➞       Flow
    ======  =======
```


### Video

To embed local videos, such as recordings of demonstrating the user interface, we require that the videos be saved as `.mp4` for greatest compatibility, usability, accessibility, and reduced file size.

Avoid animated GIFs because they do not allow control of playback.

Audio is not required, but may be helpful.
If you include audio, it is helpful to include closed captions or a transcript.

It is helpful to include overlays of key strokes, and mouse and other input gestures, to describe how to interact with the user interface.

Paths to videos must resolve in both the main documentation and the submodule's documentation, if present.
See {ref}`static-assets-label` for details.

Example MyST syntax is shown below.

````md
```{video} /_static/user-manual/blocks/block-copy-cut.mp4
```
````

Note that the path must be absolute to support both submodules and the main documentation.
Don't use file-relative paths.
The above MyST markup renders as shown below.

```{video} /_static/user-manual/blocks/block-copy-cut.mp4
```


### Diagrams and graphs with Graphviz

We use [Graphviz](https://graphviz.org/download/) and its Sphinx extension [`sphinx.ext.graphviz`](https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html) to render diagrams and graph visualizations.

The following MyST example will display as shown below.

````markdown
```{eval-rst}
.. graphviz::
    :align: center

    digraph viewstructure {
      {
        node [margin=5,shape=box]
      }
      ZCML -> {Python, Template};
    }
```
````

```{eval-rst}
.. graphviz::
    :align: center

    digraph viewstructure {
      {
        node [margin=5,shape=box]
      }
      ZCML -> {Python, Template};
    }
```


### Code block

A Python code snippet without reStructuredText options, using a simple fence.

````md
```python
a = 2
print("my 1st line")
print(f"my {a}nd line")
```
````

```python
a = 2
print("my 1st line")
print(f"my {a}nd line")
```

A Python code snippet with reStructuredText options, using a fence with the parsed reStructuredText directive `code-block`.

````md
```{code-block} python
:linenos:
:emphasize-lines: 1, 3

a = 2
print("my 1st line")
print(f"my {a}nd line")
```
````

```{code-block} python
:linenos:
:emphasize-lines: 1, 3

a = 2
print("my 1st line")
print(f"my {a}nd line")
```

### Escape literal backticks inline

```md
This is MyST syntax for term ``{term}`React` ``
```

This is MyST syntax for term ``{term}`React` ``


### Glossary terms

Add a term to the {ref}`glossary-label`, located at {file}`/glossary.md`.

```md
React
    [React](https://reactjs.org/) is a JavaScript library for building user interfaces.
    Volto, the frontend for Plone 6, uses React.
```

Reference a term in the {ref}`glossary-label`.

```md
Using {term}`React` makes frontends fun again!
```

Using {term}`React` makes frontends fun again!


### Nesting directives

You can [nest directives](https://myst-parser.readthedocs.io/en/latest/syntax/roles-and-directives.html#nesting-directives), such as [admonitions](https://myst-parser.readthedocs.io/en/latest/syntax/admonitions.html) and code blocks, by ensuring that the backtick-lines corresponding to the outermost directive are longer than the backtick-lines for the inner directives.

`````
````{tip}
To use formatted string literals ("f-strings"), begin a string with `f` or `F` before the opening quotation mark or triple quotation mark.
Inside this string, you can write a Python expression between `{` and `}` characters that can refer to variables or literal values.

```{code-block} python
:linenos:
:emphasize-lines: 1, 3

a = 2
print("my 1st line")
print(f"my {a}nd line")
```
````
`````

This would be rendered as:

````{tip}
To use formatted string literals ("f-strings"), begin a string with `f` or `F` before the opening quotation mark or triple quotation mark.
Inside this string, you can write a Python expression between `{` and `}` characters that can refer to variables or literal values.

```{code-block} python
:linenos:
:emphasize-lines: 1, 3

a = 2
print("my 1st line")
print(f"my {a}nd line")
```
````
