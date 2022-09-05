---
myst:
  html_meta:
    "description": "General Guide to Writing Documentation"
    "property=og:description": "General Guide to Writing Documentation"
    "property=og:title": "General Guide to Writing Documentation"
    "keywords": "Documentation, Plone, Sphinx, MyST, reStructuredText, Markdown"
---

(contributing-writing-docs-guide)=

# General Guide to Writing Documentation

This guide provides general help for writing documentation for Plone.


## MyST, reStructuredText, and Markdown

We use [MyST, or Markedly Structured Text](https://myst-parser.readthedocs.io/en/latest/), a rich and extensible flavor of Markdown, for authoring training documentation.

MyST extends {term}`Markdown` by incorporating all the features of {term}`reStructuredText` and {term}`Sphinx` and its extensions.
Contributors are welcome to use either Markdown or MyST syntax.

MyST may be more familiar to reStructuredText authors.
MyST allows the use of a {term}`fence` and `{rst-eval}` to evaluate native reStructuredText.
This may be useful when Markdown does not provide sufficient flexibility, such as for `figure`.


### MyST Syntax Reference

The following are frequently used snippets and examples.

```{seealso}

**Official MyST documentation**

- [The MyST Syntax Guide](https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html)
- [MyST Syntax Reference](https://myst-parser.readthedocs.io/en/latest/syntax/reference.html)
```


#### Targets and Cross-Referencing

```{seealso}
[The MyST Syntax Guide > Targets and Cross-Referencing](https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html#targets-and-cross-referencing)
```

##### Link to a Chapter or Page

```md
Here is how to set up and build the documentation locally {doc}`/contributing/setup-build`.
```

Here is how to set up and build the documentation locally {doc}`/contributing/setup-build`.


(writing-docs-guide-link-heading-label)=

##### Link to a Heading

```md
(writing-docs-guide-hello-heading-label)=

###### Hello Heading

Read the section {ref}`writing-docs-guide-link-heading-label`.
```

(writing-docs-guide-hello-heading-label)=

###### Hello Heading

Read the section {ref}`writing-docs-guide-hello-heading-label`.


##### Link to an Arbitrary Location

```md
(example-target-label)=

I have an HTML anchor above me.

Click the link to visit {ref}`my text <example-target-label>`.
```

(example-target-label)=

I have an HTML anchor above me.

Click the link to visit {ref}`my text <example-target-label>`.


##### Link to External Page

```md
Use [Shimmer](http://example.com) for cleaner whiter teeth.
```

Use [Shimmer](http://example.com) for cleaner whiter teeth.


##### Images and Figures

[Figures](https://docutils.sourceforge.io/docs/ref/rst/directives.html#figure) allow a caption and legend, whereas [images](https://docutils.sourceforge.io/docs/ref/rst/directives.html#images) do not.

Use `image` for anything but diagrams.

Use `figure` for diagrams.

Images and figures should always include `alt` text.

From [Web Accessibility In Mind (WebAIM)](https://webaim.org/techniques/alttext/):

> Alternative text serves several functions:
> - It is read by screen readers in place of images allowing the content and function of the image to be accessible to those with visual or certain cognitive disabilities.
> - It is displayed in place of the image in browsers if the image file is not loaded or when the user has chosen not to view images.
> - It provides a semantic meaning and description to images which can be read by search engines or be used to later determine the content of the image from page context alone.

Accessibility is part of the [Plone brand and identity](https://plone.org/accessibility).

````md
```{image} /_static/standards.png
:alt: XKCD "Standards" comic strip
```
````

```{image} /_static/standards.png
:alt: XKCD "Standards" comic strip
```

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


##### Code Block

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

##### Escape literal backticks inline

```md
This is MyST syntax for term ``{term}`React` ``
```

This is MyST syntax for term ``{term}`React` ``


##### Glossary terms

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


#### Toggle paragraph (Exercise solution / FAQ)

Text snippets can be hidden with the option to show. Wrap it in an `admonition` and add the `class` `toggle`.

`````
````{admonition} f-strings can make your life easier
:class: toggle

To use formatted string literals, begin a string with `f` or `F` before the opening quotation mark or triple quotation mark.
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

You can [nest directives](https://myst-parser.readthedocs.io/en/latest/syntax/roles-and-directives.html#nesting-directives), such as admonitions and code blocks, by ensuring that the backtick-lines corresponding to the outermost directive are longer than the backtick-lines for the inner directives.

This would be rendered as:

````{admonition} f-strings can make your life easier
:class: toggle

To use formatted string literals, begin a string with `f` or `F` before the opening quotation mark or triple quotation mark.
Inside this string, you can write a Python expression between `{` and `}` characters that can refer to variables or literal values.

```{code-block} python
:linenos:
:emphasize-lines: 1, 3

a = 2
print("my 1st line")
print(f"my {a}nd line")
```
````


## Abridged Plone Documentation Styleguide

Guides should be informational, but friendly.

Address the reader by using "you" instead of "the user".

Avoid contractions, and spell out the words.
For example, use "do not" instead of "don't".

Please do not follow PEP8 maximum line length standard.
Documentation is narrative text and images, not Python code.

Use one sentence per line.
Keep sentences short and understandable.
This will greatly improve the editing and maintenance of your documentation.


## General Documentation Writing References

- [Write the Docs - Documentation Guide](https://www.writethedocs.org/guide/)
- [A Guide to Em Dashes, En Dashes, and Hyphens](https://www.merriam-webster.com/words-at-play/em-dash-en-dash-how-to-use)


### English grammar, spelling, punctuation, and syntax

Because it is difficult to automate good English grammar and syntax, we do not strictly enforce it.
We also understand that contributors might not be fluent in English.
We encourage contributors to make a reasonable effort, and to seek help from community members who are fluent in English.
Please ask!
