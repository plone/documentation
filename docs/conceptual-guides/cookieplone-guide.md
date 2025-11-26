# Cookieplone Conceptual Guide

## Introduction

Cookieplone is an essential tool for creating new Plone projects. Instead of manually setting up folders, configuration files, and boilerplate code, Cookieplone uses the **Cookiecutter** template system to instantly generate a complete, production-ready Plone project with modern practices.

It helps you:

- Bootstrap Plone backend + Volto frontend quickly  
- Avoid common setup errors  
- Maintain a standard and scalable project structure  
- Use ready-made Docker, CI, and deployment configurations  

---

## 1. Cookieplone Workflow

The workflow takes you from a blank state to a fully running Plone development environment.


### Workflow Diagram

```{mermaid}
graph TD
   A[Start: Run Cookiecutter Command] --> B{Answer Project Questions};
   B --> C(Generate Complete Project Structure);
   C --> D[Navigate to Project Folder];
   D --> E[Run Project Setup (e.g., make install)];
   E --> F[Start Development Servers (e.g., make start)];
   F --> G(Project is Running);
```

---

## 2. Clarifying Setup Variables 

During project generation, Cookieplone prompts you for several important configuration values. These directly influence your CI/CD and deployment setup.

### `github_organization`

- Defines the namespace/organization where your project will live.  
- Usually your GitHub or GitLab username/organization.  
- Used in configuring automatic CI pipelines and repository metadata.

### `container_registry`

- Specifies where Docker images will be stored and pulled from.  
- Common options include:  
  - Docker Hub  
  - GitHub Container Registry  
  - GitLab Registry  

These values help structure deployment workflows automatically.

---

## 3. Essential Development Tools (`make` Commands)

Cookieplone provides helpful `make` commands to simplify local development.

### Make Commands Table

| Command | Purpose |
|---|---|
| `make build` | Builds backend + frontend Docker images. Necessary after major dependency changes. |
| `make start` | Starts the full Plone setup (backend + Volto) using Docker Compose. |
| `make stop` | Stops containers gracefully without removing them. |
| `make install` | Installs Python and JavaScript dependencies inside containers. Useful during the first project setup. |

---

## ⚠️ Critical Warning About `make clean` 

> **Warning:**  
> `make clean` removes temporary build files **and important local project data**, including:  
> - The Plone database  
> - Cached configuration  
> - Local environment artifacts  
>
> Only use `make clean` when you want to fully reset your local project environment.

For most minor issues, prefer:

- `make stop` – stops containers safely  
- `make start` – restarts the Plone environment