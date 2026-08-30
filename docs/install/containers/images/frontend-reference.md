---
myst:
  html_meta:
    "description": "Reference for plone/plone-frontend image environment variables"
    "property=og:description": "Reference for plone/plone-frontend image environment variables"
    "property=og:title": "Plone Frontend image - Environment Variables Reference"
    "keywords": "Plone 6, install, installation, docker, containers, plone/plone-frontend, reference, environment variables"
---

# `plone/plone-frontend` - Environment Variables Reference

This reference document covers all environment variables available for the Plone frontend [Docker](https://www.docker.com/) image.

For usage instructions and examples, see {doc}`frontend`.


## Main variables

| Environment variable | Description | Example |
| --- | --- | --- |
| `RAZZLE_API_PATH` | Used to generate frontend calls to the backend. Needs to be a public URL accessible by client browser. | `http://api.site.org/++api++/` |
| `RAZZLE_INTERNAL_API_PATH` | Used by the middleware to construct requests to the backend. It can be a non-public address. | `http://backend:8080/Plone` |
| `VOLTO_ROBOTSTXT` | Override the `robots.txt` file. | `"User-agent: *\nDisallow: "` |

```{note}
For an extensive list of environment variables used by the frontend, visit {doc}`/volto/configuration/environmentvariables`.
```

