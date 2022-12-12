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

## High Level Overview for Developers

Plone is a content management platform with its backend written in Python. The backend builds upon Zope, an open source web 
application server and development system, and thus on the pluggable Zope Component Architecture (ZCA). The frontend has up until version 6
served HTML based content, with advanced resource management on the server to add and bundle CSS and javascript. 

With the release of Plone 6 there are now two out of the box supported configurations possible for a new Plone website.

You can still use the Python based backend server to render the content server side and deliver html to the browser.
This setup is referred to in the documentation as 'Classic UI' and has been supported by Plone since its release. 
For container based deployment you only need the plone-backend image, or a derivation with your customisations added.
In the documentation 

The default and advised configuration for new websites in Plone is to use our new React Based javascript frontend called 'Volto'.
For this setup you still need to run the Python based backend server, but with the REST API enabled and an updated configuration profile.
In addition a separate NodeJS based frontend server will serve the javascript frontend resources and provide SSR with hydration.
To deploy this setup using containers you will need the plone-frontend image of the frontend server. 

This is the first release of Plone where we support two programming language stacks, one for Python and Javascript.
The documentation has been rewritten, but for this first release you will find some repetition of concepts in the documentation structure. 
For example for the development setup and information on deployment options.
It will take some time before we find and can implement the best structure to explain these new possibilities and expansion of Plone its capabilities.


(overview-5-label)=
## Deployment

To run a public Plone website in production, you will also need to configure and run a reverse proxy (or ingress), arrange for SSL certificates (either from Lets Encrypt or manually), check persistenct of the content database and arrange for backups. This is the domain
of sysadmins and modern devops.  Our documentation contains setup examples for these services but requires also experience and knowledge.


(overview-6-label)=
## Good to know / What to know

One of the key benefits of the new React based frontend for Plone 6 is that you can now customise and theme Plone extensively using HTML and Javascript using up to date frontend technologies without having having to set up a local Python development environment.
The Plone backend can be run on a local developer machine in a container.

Basic familiarity with programming in Python and managing Python modules/packages using virtualenv and pip is required to work on the backend code.
We use virtualenv and mxdev to manage the source installation of packages in Plone 6.

Similarly, to develop for the new React frontend, you need to have some experience with setting up NodeJS, using a tool like NVM (Node Version Manager) to isolate your setup, Yarn and React. 

If you are looking for more study material on these technologies and the documentation  is too dense, see and follow one or more [Plone Trainings]](https://training.plone.org).
Our trainings are more verbose and contain extra clarification and examples. 


```{toctree}
:maxdepth: 2
:hidden:


```
