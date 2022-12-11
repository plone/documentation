---
myst:
  html_meta:
    "description": "Plone 6 overview"
    "property=og:description": "Plone 6 overview"
    "property=og:title": "Plone 6 overview"
    "keywords": "Plone 6, overview"
---

(overview-label)=

# Overview

````{todo}
This page needs content.
```{seealso}
[Issue #1352](https://github.com/plone/documentation/issues/1352)
```
````

(overview-2-label)=

## Overview

Plone is a mature, secure, and user-friendly content management system (CMS).
Plone was first released to the public on October 4, 2001.

Plone has the maturity, stability, and reliability of an application maintained by open source developers with decades of experience, while continually evolving and adapting to modern technology.

Lots of customizations can be made trough-the-web, such as creating content types, themes, workflows, and much more.
A full filesystem based development workflow is also possible.
Plone may be extended and used as a framework on which to build custom CMS-like solutions.

Plone works as a:

- Full-featured server-side rendered HTML CMS.
- React-based frontend for editing and viewing content, backed by a server with a REST API.
- Headless CMS server with a REST API, allowing a developer to build a custom frontend with their chosen technology.




(overview-3-label)=

## Key benefits

Security is built into Plone's architecture from the ground up.
Plone offers fine-grained permission control over content and actions.

Plone is easy to set up compared to other CMS'es in its category, extremely flexible, and provides you with a system for managing web content that is ideal for project groups, communities, websites, extranets, and intranets.

- **Plone empowers content editors and web application developers.**
  The Plone Team includes usability experts who have made Plone easy and attractive for content managers to add, update, and maintain content.

- **Plone is international.**
  The Plone interface has more than 35 translations, and tools exist for managing multilingual content.

- **Plone follows standards and is inclusive.**
  Plone carefully follows standards for usability and accessibility.
  Plone is compliant with WCAG 2.1 level AA and aims for ATAG 2.0 level AA.

- **Plone is open source.**
  Plone is licensed under the GNU General Public License, the same license used by Linux.
  This gives you the right to use Plone without a license fee, and to improve upon the product.

- **Plone is supported.**
  There are over two hundred active developers in the Plone Development Team around the world, and a multitude of companies that specialize in Plone development and support.

- **Plone is extensible.**
  There is a multitude of add-on products for Plone to add new features and content types.
  In addition, Plone can be scripted using web standard solutions and open source languages.

- **Plone is technology neutral.**
  Plone can interoperate with most relational database systems—both open source and commercial—and runs on a vast array of
  platforms, including Linux, Windows, macOS, and BSD.



(overview-4-label)=

## High Level Overview

Plone is a content management platform with its backend written in Python. The backend builds upon Zope, an open source web 
application server and development system, and thus on the pluggable Zope Component Architecture (ZCA). The frontend has up until now
served HTML based content, with advanced resource management on the server to add and bundle CSS and javascript. 

With the release of Plone 6 there are now two out of the box supported configurations possible for a new Plone website.

You can still use the Python based backend server to render the content server side and deliver html to the browser.
This setup is referred to in the documentation as 'Classic UI' and has been supported by Plone since its release. 
For container based deployment you only need the plone-backend image, or a derivation with your customisations added. 

The default and advised configuration for new websites in Plone is to use our new React Based javascript frontend called 'Volto'.
For this setup you will still need to run the Python based backend server, but with the REST API enabled and an updated configuration profile.
In addition a separate NodeJS based frontend server will serve the javascript frontend resources and provide SSR with hydration.
To deploy this setup using containers you will need the plone-frontend image of the frontend server. 

This is the first release of Plone where the community has to work in and support 2 language and development stacks.
The documentation has been rewritten, but for this first release you will find some repetition of concepts in the documentation structure. 
For example for deployment or development setup.
It will take some time before we will find the best structure to explain these new possibilities and expansion of Plone its capabilities.


(overview-5-label)=

### Traditional server side rendered HTML pages


(overview-6-label)=

### Headless CMS with JavaScript frontend through a REST API


(overview-7-label)=

### Explain frontend-backend terms


(overview-8-label)=

### Security


(overview-9-label)=

### Accessibility (a11y)


(overview-10-label)=

### Internationalization (i18n)



```{toctree}
:maxdepth: 2
:hidden:

history
```
