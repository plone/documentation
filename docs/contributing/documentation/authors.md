---
myst:
  html_meta:
    "description": "Authors' guide to writing Plone Documentation. It covers configuring quality checks and syntax for writing markup that is of particular interest to authors."
    "property=og:description": "Authors' guide to writing Plone Documentation. It covers configuring quality checks and syntax for writing markup that is of particular interest to authors."
    "property=og:title": "Authors Guide"
    "keywords": "Plone, Documentation, SEO, meta, Vale, spell, grammar, style, check, linkcheck, lexer"
---

(authors-guide-label)=

# Authors guide

This guide is for authors of Plone Documentation.
It covers how to run a live preview of documentation while editing, build documentation, and perform quality checks.
For general markup syntax, see {doc}`myst-reference`.


## Synchronize the browser while editing

The following shell command rebuilds documentation as you edit its files, with live reload in the browser.

```shell
make livehtml
```

The console will give you the URL to open in a web browser.
The URL may vary, according to its configuration in the repository's {file}`Makefile`.

```console
[sphinx-autobuild] Serving on http://127.0.0.1:8050
```


## Editor tools

-   [MyST-Markdown VS Code Extension](https://marketplace.visualstudio.com/items?itemName=ExecutableBookProject.myst-highlight)


(authors-quality-checks-label)=

## Quality checks

We strive for high quality documentation, setting the following minimum standards.


(authors-markup-syntax-label)=

### Markup syntax must be valid

See both the specific markup syntax above and general markup in {doc}`myst-reference`.

To validate markup, run the following command.

```shell
make html
```

The console will report any errors.
You should fix the errors for those pages that you edit.


### Override `html` build configuration options

Sphinx supports overriding configuration options.
The following examples serve as tips for spotting mistakes in your documentation when you have too many errors or warnings.

In Sphinx, you can use the `SPHINXOPTS` environment variable to set [configuration options](https://www.sphinx-doc.org/en/master/usage/configuration.html) of [`sphinx-build`](https://www.sphinx-doc.org/en/master/man/sphinx-build.html).
Syntax is in the following form.

```shell
make SPHINXOPTS="OPTION VALUE" BUILDER
```

The following example shows how to clean then build a live HTML preview of the documentation while suppressing syntax highlighting failures.

```shell
make SPHINXOPTS="-D suppress_warnings='misc.highlighting_failure'" clean livehtml
```


(authors-english-label)=

### Vale for American English spelling, grammar, and syntax, and style guide

[Vale](https://vale.sh/) is a linter for narrative text.
It checks spelling, English grammar and syntax, and style guides.
Plone uses American English.

The Plone Documentation Team selected the [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/) for its ease of use—especially for non-native English readers and writers—and attention to non-technical audiences. 

To perform all these checks, run the following command.

```shell
make vale
```

Because it is difficult to automate good American English grammar and syntax, it is not strictly enforced.
We also understand that contributors might not be fluent in English.
If you are more comfortable writing in your preferred language, then you may submit a pull request written in your language, and the Documentation Team will use translation tools to translate it to English.
We encourage contributors to make a reasonable effort, and to request a review of their pull request from community members who are fluent in English to fix grammar and syntax.
Please ask!

```{note}
More corrections to spellings and Vale's configuration are welcome by submitting a pull request.
This is an easy way to become a contributor to Plone.
See {ref}`authors-advanced-vale-usage-label` for details.
```


(authors-advanced-vale-usage-label)=

#### Advanced Vale usage

You can pass options to Vale in the `VALEOPTS` and `VALEFILES` environment variables.
In the following example, you can run Vale to display warnings or errors only, not suggestions, in the console on a single file.

```shell
make vale VALEOPTS="--minAlertLevel='warning'" VALEFILES="docs/index.md"
```

The command `make vale` automatically installs Vale into your Python virtual environment—which is also created via any documentation `Makefile` commands—when you invoke it for the first time.

Vale has [integrations](https://vale.sh/docs/) with various IDEs.
Integration might require installing Vale using operating system's package manager.

-   [JetBrains](https://plugins.jetbrains.com/plugin/19613-vale-cli/docs)
-   [Vim](https://github.com/dense-analysis/ale)
-   [VS Code](https://github.com/chrischinchilla/vale-vscode)

Plone configures Vale in three places:

-   {file}`.vale.ini` is Vale's configuration file.
    This file allows overriding rules or changing their severity.
-   {file}`Makefile` passes options to the `vale` command, such as the files Vale checks.
-   Plone documentation uses a custom spelling dictionary, with accepted and rejected spellings in {file}`styles/config/vocabularies/Plone/`.
    Authors should add new words and proper names using correct casing to {file}`styles/config/vocabularies/Plone/accept.txt`, sorted alphabetically and case-insensitive.

    If Vale does not reject a spelling that should be rejected, then you can add it to {file}`styles/config/vocabularies/Plone/reject.txt`.
-   You can add additional spellings to accept or reject in their respective files inside the {file}`styles/config/vocabularies/Base/` folder.


(authors-linkcheck-label)=

### All links must be valid

```{important}
Before you add a link, consider whether you really need it for the documentation.
Avoid linking to blog posts because they rapidly succumb to bit rot.
It is preferable to copy the content from the source and add a link to the source as a reference through a `seealso` admonition, than to merely link to the source.
```

Valid links are enforced automatically through Sphinx's `linkcheck` builder.
To validate links, run the following command.

```shell
make linkcheckbroken
```

Only broken links will show in the console output.
Open `/_build/linkcheck/output.txt` for a list of all links that were checked and their result.

[Configuration of the `linkcheck` builder](https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-linkcheck-builder) is in {file}`Makefile` and {file}`docs/conf.py`.

When you add a link to the documentation, it must be a valid public URL without requiring authentication.

If a link has succumbed to bit rot, then try finding the most recently scraped version on the [Internet Archive Wayback Machine](https://web.archive.org/), and update the link.

If it is not a valid link, or is private or local, then you must exclude it from `linkcheck`.
You can do so by wrapping it in single backticks in the page.

```{example}
Visit the URL `http://www.example.com` for an example.
```

Alternatively, you can add it to the `linkcheck_ignore` list in {file}`conf.py`.
`linkcheck_ignore` supports regular expression syntax.

```python
linkcheck_ignore = [
    r"http://0.0.0.0",
]
```

```{danger}
Please do not abuse `linkcheck_ignore`.

There is a special place in hell reserved for contributors who do not bother to update bad links, either dead ones or redirects, causing `linkcheck` to fail.
And there is a doubly punishing place for those who disable `linkcheck` because there are too many bad links.

Please do not be "that person".
```


(authors-syntax-highlighting-label)=

### Syntax highlighting

Pygments provides syntax highlighting in Sphinx.

When including code snippets, you should specify the language.
Authors must use a proper [Pygments lexer](https://pygments.org/docs/lexers/) and not generate warnings.

The snippet must be valid syntax for the language you specify, else it will not be highlighted properly.
Avoid adding comments to code snippets, unless you use valid comment syntax for that language.
For example, JSON does not allow comments.

Do not indicate elided or omitted code with ellipses (`...` or `…`).
These are almost never valid syntax and will cause syntax highlighting to fail for the code block.

````{note}
There are some known issues with syntax highlighting with the lexers for `jsx`, `less`, and `scss`.
Try your best to fix the code example.

```{seealso}
-   [WARNING: Lexing literal_block ... as "jsx" resulted in an error at token: "'". Retrying in relaxed mode.](https://github.com/pygments/pygments/issues/2816)
-   [LESS lexer marks nested `.` and `h2` as invalid](https://github.com/pygments/pygments/issues/2817)
-   [WARNING: Lexing literal_block ... as "scss" resulted in an error at token: '$'](https://github.com/pygments/pygments/issues/2818)
```
````


#### Choose a Lexer

Some lexers are less than perfect.
If your code block does not highlight well, then consider specifying a less ambitious lexer, such as `text`.

Use `shell` for commands to be issued in a terminal session.
Do not include shell prompts.
This will make commands easy to copy and paste for readers.

Use `console` for output of a shell session.
If you have a mix of a shell command and its output, then use `console`.

If `xml` does not work well, then try `html`.

`jsx` has a complex syntax that is difficult to parse.

The lexers `html+ng2`, `scss`, `http`, `less` are also suboptimal and particular.

If no other lexer works well, then fall back to `text`.
At least then the build will succeed without warnings, although syntax highlighting for such snippets will not appear.


#### Validate the lexer

Always build the page to validate syntax.
The change should not be merged if there are any Sphinx warnings.
The Sphinx console will display any warnings, such as the following.

```console
/Plone/documentation/classic-ui/bodyclasses.md:10: WARNING: Could not lex literal_block as "python". Highlighting skipped.
```

The above warning indicates that the syntax is not valid.
Common mistakes include the following.

-   Using `...` or `…` to indicate omitted code.
    It is preferable to never use ellipses.
    If you must do that, comment it out using the language's comment syntax.
-   Using comments in JSON.
-   A previous code block bleeds through to the next due to invalid MyST syntax.

To validate code block syntax of a page you edit, run the following command.

```shell
make html
```

An [online demo of all lexers that Pygments supports](https://pygments.org/demo/) may be helpful to test out your code blocks and snippets for syntax highlighting.
You can also use the [`pygmentize`](https://pygments.org/docs/cmdline/) binary.

When using the online lexer, if any red-bordered rectangles appear, then the lexer for Pygments interprets your snippet as not valid.
You can search the [Pygments issue tracker](https://github.com/search?q=repo%3Apygments%2Fpygments+&type=issues) for possible solutions, or submit a pull request to enhance the lexer.


(authors-html-meta-data-label)=

### HTML and Open Graph metadata

All documents must have a `myst` topmatter key with an `html_meta` directive at the top of every page.

When you create a new page, you can either copy an existing page that has the `html_meta` information, or you can create an empty file and run a `make` command to add a metadata section as shown.

```shell
touch path-to-file/my-file.md
make html_meta
```

When rendered to HTML, the `html_meta` directive inserts `<meta>` tags for improved search engine results and nicer social media posts.
Authors should include at least `description`, `property=og:description`, `property=og:title`, and `keywords` meta tags.

The following is an example of `html_meta`.
Note that the content of the two tags `description` and `property=og:description` should be identical.

% Cannot use sphinx-examples for this one.

```md
---
myst:
  html_meta:
    "description": "Authors' guide to writing Plone Documentation. It covers configuring quality checks and syntax for writing markup that is of particular interest to authors."
    "property=og:description": "Authors' guide to writing Plone Documentation. It covers configuring quality checks and syntax for writing markup that is of particular interest to authors."
    "property=og:title": "Authors Guide"
    "keywords": "Plone, Documentation, SEO, meta, Vale, spell, grammar, style, check, linkcheck, lexer"
---
```

This renders in the HTML `<head>` section as follows.

```html
<meta content="Authors' guide to writing Plone Documentation. It covers configuring quality checks and syntax for writing markup that is of particular interest to authors." name="description" />
<meta content="Authors' guide to writing Plone Documentation. It covers configuring quality checks and syntax for writing markup that is of particular interest to authors." property="og:description" />
<meta content="Authors Guide" property="og:title" />
<meta content="Plone, Documentation, SEO, meta, Vale, spell, grammar, style, check, linkcheck, lexer" name="keywords" />
```

Additional {term}`Open Graph` metadata is implemented through the Sphinx extension [`sphinxext-opengraph`](https://github.com/wpilibsuite/sphinxext-opengraph) and the [MyST `html_meta` directive](https://myst-parser.readthedocs.io/en/latest/configuration.html#setting-html-metadata), which resolves to the [Docutils `meta` directive](https://docutils.sourceforge.io/docs/ref/rst/directives.html#metadata).
See the site-wide configuration in {file}`conf.py`.


## Diátaxis framework

Plone Documentation uses the {term}`Diátaxis framework`, a systematic approach to technical documentation authoring.
Rather than attempt to organize documentation toward a specific role such as "developer", "user", or "administrator", the Diátaxis framework organizes documentation into the four categories of tutorials, how-to guides, explanation, and reference.
In this way, your title or role does not matter.
Instead, what you want to achieve matters.
By keeping each page focused on one category, readers can focus on getting work done, understanding, or experimenting.

Although Plone 6 Documentation is not completely aligned with the Diátaxis framework, it is gradually moving toward it.


## Plone documentation styleguide

We follow [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/).

Key concepts from that guide include the following.

-   Documentation should be informational, but friendly.
-   Address the reader by using "you" and "your" instead of "the user" or "the user's".
-   When giving instructions, use the [imperative](https://learn.microsoft.com/en-us/style-guide/grammar/verbs#mood-of-verbs).
-   Use the [active voice](https://learn.microsoft.com/en-us/style-guide/grammar/verbs#active-and-passive-voice) whenever possible, avoiding the passive voice.
-   Headings should be "Sentence cased", not "Title Cased".

The Plone Documentation Team adopted additional guidelines.

-   Use one sentence per line.
    Keep sentences short and understandable.

    Never break a single sentence across multiple lines.
    Documentation is narrative text and images, not code.
    Do not follow the PEP8 maximum line length standard.
    Similarly, never use English semantic line breaks.
    English semantic rules are difficult to understand and enforce.

    Not following this guidance makes pull request reviews needlessly difficult, often resulting in noisy diffs.

    The reviewer can't give targeted feedback for a single sentence when there are multiple sentences on one line.
    
    When a single sentence is broken across multiple lines, the reviewer may not know that they can submit [one suggestion for multiple lines](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/commenting-on-a-pull-request#adding-comments-to-a-pull-request).
    Instead, they either make a comment or a single suggestion leaving the author to manually edit the lines.
    This in turn deprives you of the easy option to commit the suggestion to the pull request by a single click of a button in the GitHub user interface.

    Following this guidance will greatly improve the editing and maintenance of your documentation.

-   Have the file [`.vscode/settings.json`](/_static/settings.json) in the root of your project to prevent VSCode from reformatting files with the `.md` extension. 

-   Use dashes `-` in filenames and avoid underscores.
-   Images should be no wider than 740 pixels to fit within the documentation's main view port.
    This avoids scaling and reducing legibility of images.
    To make that work in Volto, set your browser width to 1180 pixels.
    You will notice that the drag and trash icons for each block move inside the block from outside.
    
    If you create images wider than 740 pixels, then you must use image display enhancement as described in {ref}`enhance-media-label`.
-   In user documentation, provide screenshots of each step where the interface changes.
    It is painstaking, but worth the effort.
    Provide sufficient detail of what each option is and does.


## General documentation writing references

-   [Diátaxis framework](https://www.diataxis.fr/)
-   [Write the Docs - Documentation Guide](https://www.writethedocs.org/guide/)
-   [Creating effective technical documentation](https://developer.mozilla.org/en-US/blog/technical-writing/), Dipika Bhattacharya, Technical Writer at Mozilla Developer Network
-   [A Guide to Em Dashes, En Dashes, and Hyphens](https://www.merriam-webster.com/grammar/em-dash-en-dash-how-to-use)
