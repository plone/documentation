---
myst:
  html_meta:
    "description": "PLIP review"
    "property=og:description": "PLIP review"
    "property=og:title": "PLIP review"
    "keywords": "PLIP, review, Plone Improvement Proposal, Plone"
---

# PLIP review

A Plone Improvement Proposal (PLIP) is a formal process to propose a change to improve Plone.
A review of a PLIP ensures that proposed behavior has been implemented as expected.

Post your PLIP review as a comment in the PLIP pull request.


## Set up the environment

Follow the instructions in {doc}`index`.
You will need to checkout the branch to which the PLIP is assigned.
Instead of running the buildout with the default buildout file, you will run the configuration specific to that PLIP:

```shell
./bin/buildout -c plips/plip-<repo>-<issue>-<branch>.cfg
```


## Functionality review

This section describes the topics that may be addressed in a PLIP review, depending on the nature of the PLIP itself.

Report bugs or issues you find during the review on GitHub as you would for any Plone bug.
Reference the PLIP in the bug, assign it to its implementer, and add a tag for the PLIP in the form of `plip-xxx`.
This way the implementer can find help if they need it.
Also set a priority for the ticket.
The PLIP will not be merged until all blockers and critical bugs are fixed.


### General

-   Take screenshots or videos as necessary, and post them to the pull request with your comments.
-   Does the PLIP actually do what the implementers proposed?
-   Are there incomplete variations?
-   Were there any errors running buildout?
-   If there were migrations, did they work?
-   Do error and status messages make sense?
-   Are messages properly internationalized?
-   Are there any performance considerations?


### Bugs

-   Are there any bugs?
-   Do fields handle unexpected data?
-   Is validation function correctly and make sense?
-   Is validation too restrictive or not restrictive enough?


### Usability issues

-   Is the implementation usable?
-   How will end users respond to the change?
-   Does this PLIP need a usability review?
    If you think this PLIP needs a usability review, add GitHub issue labels {guilabel}`99 tag: UX`, or similar, and {guilabel}`32 needs: review`, and add a note in the comments.
-   Is the PLIP consistent with the rest of Plone?
    For example, if there is control panel configuration, does the new form fit in with the rest of the panels?
-   Does everything flow nicely for all users?
-   Are there any new permissions and do they work properly?
-   Does permission assignment to roles make sense?


### Documentation issues

-   Is the corresponding documentation for the end user, be it developer or Plone user, sufficient?
-   Is the change itself properly documented?


## Code review

This section describes considerations of code quality.


### Python

-   Is this code maintainable?
-   Is the code properly documented?
-   Does the code adhere to formatting and style standards?
-   Are there any imported deprecated modules?


### JavaScript

-   Does the JavaScript satisfy the package's JavaScript standards, or if the package has no standard, then Plone's?
    See Plone's section about {doc}`plone5:develop/addons/javascript/index` and the {doc}`plone5:develop/styleguide/javascript`.
-   Does the JavaScript work in all currently supported browsers?
-   Is the JavaScript performant?

```{todo}
Update links from Plone 5 Documentation to Plone 6 Documentation, when they exist.
See https://github.com/plone/documentation/issues/1330
```

### ME/TAL

-   Does the PLIP use views appropriately, avoiding too much logic?
-   Is there any code in a loop that could potentially be a performance issue?
-   Are there any deprecated or old style ME/TAL lines of code, such as using `DateTime`?
-   Is the rendered HTML compliant with standards?
-   Are `id`s and classes used appropriately?
