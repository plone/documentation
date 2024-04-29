---
myst:
  html_meta:
    "description": "Components of a Plone 6 application for deployment"
    "property=og:description": "Components of a Plone 6 application for deployment"
    "property=og:title": "Components of a Plone 6 application for deployment"
    "keywords": "Plone, deployment, components, backend, volto, fronted, TLS termination proxy, load balancer, router, database, mail service, optimization, maintenance"
---

(deployment-components-label)=

# Components

This page in the deployment guide covers the components in a Plone application deployment.
The components can be broken down into those that are required, recommended, and optional.


(deployment-required-components-label)=

## Required components

You need the following components to deploy a Plone application.

-   {term}`Plone backend`
-   {term}`Volto` as the default {term}`Frontend` for Plone
-   {term}`TLS termination proxy`
-   {term}`Load balancer` or router
-   Database
-   Mail service
-   Maintenance tasks
    -   Database backup
    -   Packing database - https://5.docs.plone.org/manage/deploying/packing.html
    -   Monitoring
    -   Log rotation
    -   Firewall
    -   Attack protection
    -   DNS
    -   Host name resolution


(deployment-recommended-components-label)=

## Recommended components

Recommended components, although not required, will help with the performance and user experience of your Plone application.

-   HTTP caching


(deployment-optional-components-label)=

## Optional components

-   Search

