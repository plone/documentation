---
myst:
  html_meta:
    "description": "Miscellaneous contributor contributed recipes for content types and schema in Plone"
    "property=og:description": "Miscellaneous contributor contributed recipes for content types and schema in Plone"
    "property=og:title": "Miscellaneous contributor contributed recipes for content types and schema in Plone"
    "keywords": "Plone, miscellaneous, recipes, content types"
---

# Miscellaneous recipes

## Hiding a field

On occasion you may want to hide a field in a schema without modifying the original schema.
To do this, you can use tagged values on the schema.
In this example, you would hide the `introduction` and `answers` fields:

```python
from example.package.content.assessmentitem import IAssessmentItem
from plone.autoform.interfaces import OMITTED_KEY
IAssessmentItem.setTaggedValue(OMITTED_KEY,
                           [(Interface, "introduction", "true"),
                            (Interface, "answers", "true")])
```

This code can reside in {file}`another.package.__init__.py`.
