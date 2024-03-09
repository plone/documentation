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

Plone is a content management system (CMS) that is well-known for its user-friendly interface and robust security features. 
With Plone, even non-technical users can easily create and manage the content for a public website or intranet using only a web browser. 
Plone's intuitive interface and comprehensive set of features make it a popular choice for businesses, governments, universities, and any organization that needs a reliable and easy-to-use CMS.

Plone has a long history and has been trusted by users around the world since its initial release on October 4, 2001. 
Over the years, Plone has undergone many improvements and enhancements, making it a highly mature and stable CMS. 
Additionally, Plone is supported by a strong community of users and developers who contribute to its ongoing success.

Plone has the maturity, stability, and reliability of an application maintained by open source developers with decades of experience, while continually evolving and adapting to modern technology.

Lots of customizations can be made through-the-web, such as creating content types, themes, workflows, and much more.
A full file system based development workflow is possible and recommended for team work and deployment, backed by source code repositories.
Plone can be extended and used as a framework on which to build custom CMS-like solutions.

Plone works as a:

- Full-featured server-side rendered HTML CMS.
- React-based frontend for editing and viewing content, backed by a server with a REST API.
- Headless CMS server with a REST API, allowing a developer to build a custom frontend with their chosen technology.

(overview-3-label)=

## Key benefits

Security is built into Plone's architecture from the ground up.
Plone offers fine-grained permission control over content and actions.

Plone is easy to set up compared to other CMSs in its category, extremely flexible, and provides you with a system for managing web content that is ideal for project groups, communities, websites, extranets, and intranets.

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
  Plone can interoperate with most relational database systems—both open source and commercial—and runs on many platforms, including Linux, Windows, macOS, and BSD.



(overview-4-label)=

## High Level Overview for Developers

Plone is a content management platform with its backend written in Python.
It is built on top of the open source Zope web application server and development system. 
Plone makes use of the pluggable Zope Component Architecture (ZCA) to provide a highly modular and extensible system.
Throughout its history, Plone has used {term}`server-side rendering` to generate HTML-based content, with advanced resource management features for adding and bundling CSS and JavaScript. 
Additionally, Plone's use of a component architecture makes it easy to extend and customize, allowing users to create unique, feature rich websites that are tailored to their specific needs.

With the release of Plone 6, you now have the option to choose from two different out-of-the-box supported configurations when setting up a new Plone website.
The Python-based backend server in Plone can still be used alone to render content server-side and deliver HTML to the browser, a setup that is referred to in the Plone documentation as "Classic UI". 
This configuration has been supported by Plone since its initial release and is still available in the latest version of the platform.
For container-based deployment, only the `plone-backend` image is required.
It may be used as a base image, adding customizations, to make a derivative image.

The default and recommended configuration for new websites in Plone is the new React-based JavaScript frontend called "Volto".
For this setup you still need to run the Python-based backend server, as well as enable the REST API, and update the configuration profile.
These settings and profile are applied automatically when you select the {guilabel}`Create Plone Site` option in the Plone website creation form.
In addition a separate NodeJS based frontend server will serve the JavaScript frontend resources and provide {term}`SSR` with {term}`hydration`.
To deploy this setup using containers, you will need the `plone-frontend` image for the frontend server.

Beginning with Plone 6, we now support two programming language stacks, one each for Python and JavaScript.
The documentation has been rewritten, but for this first release you will find some repetition of concepts in the documentation structure.
See, for example, the development setup and information on deployment options.
It will take some time until we find and can implement the best structure to explain these new possibilities and the expansion of Plone's capabilities.

```{seealso}
https://training.plone.org/mastering-plone/what_is_plone.html
```


(overview-5-label)=
## Deployment

To run a public Plone website in production, you will also need to configure and run a reverse proxy (or ingress), arrange for SSL certificates (either from Let's Encrypt or manually), guarantee persistence of the content database, and arrange backups.
This is the domain of systems administrators and modern developer-operations professionals.
Our documentation contains setup examples for these services, yet requires that the reader have some generic experience and knowledge of these domains.


(overview-6-label)=
## Good to know / What to know

One of the key benefits of the new React-based frontend for Plone 6 is that you can now customize and theme Plone extensively using HTML, CSS, and JavaScript using up-to-date frontend technologies without having to set up a local Python development environment.
The Plone backend can be run on a local developer machine in a container.

Basic familiarity with programming in Python and managing Python modules and packages using `virtualenv` and `pip` is required to work on the backend code.
We use `virtualenv` and {term}`mxdev` to manage the source installation of packages in Plone 6.

Similarly, to develop for the new React frontend, you need to have some experience with setting up NodeJS, using a tool like NVM (Node Version Manager) to isolate your setup, and familiarity with {term}`Yarn` and {term}`React`.

If you are looking for more study material on these technologies beyond the documentation, see and follow one or more [Plone Trainings](https://training.plone.org).
Our trainings are more verbose and contain extra clarification and examples.
