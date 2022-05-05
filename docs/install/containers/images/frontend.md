---
html_meta:
  "description": "Using plone/plone-frontend image"
  "property=og:description": "Using plone/plone-frontend image"
  "property=og:title": "Plone Frontend image"
  "keywords": "Plone 6, install, installation, docker, containers"
---

# plone/plone-frontend

Plone 6 default frontend [Docker](https://docker.com) image using Node. The frontend is written using React and requires a Plone backend to be running and accessible.

This image is not a **base image** to be extended in your projects, but an example of how Plone UX works out of the box.

## Using this image

## Configuration Variables

### Main variables


| Environment variable        | Description                                                                                               | Example                         |
| --------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------- |
| RAZZLE_API_PATH             | Used to generate frontend calls to the backend. Needs to be a public url accessible by client browser     | http://api.site.ort/++api++/    |
| RAZZLE_INTERNAL_API_PATH    | Used by the middleware to construct requests to the backend. It can be a non-public address               | http://backend:8080/Plone       |
| VOLTO_ROBOTSTXT             | Override the robots.txt file                                                                              | "User-agent: *\nDisallow: "     |

```{note}
For an extensive list of environment variables used by the frontend, visit the Volto documentation.
```





## Versions

For a complete list of tags and versions, visit the [plone/plone-frontend page on dockerhub](https://hub.docker.com/r/plone/plone-frontend)

## Contribute

- [Issue Tracker](https://github.com/plone/plone-frontend/issues)
- [Source Code](https://github.com/plone/plone-frontend/)
- [Documentation](https://github.com/plone/plone-frontend/)
