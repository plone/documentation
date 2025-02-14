---
myst:
  html_meta:
    "description": "Reference guide for all make commands used in Cookieplone."
    "property=og:description": "Reference guide for all make commands used in Cookieplone."
    "property=og:title": "Cookieplone Make Commands"
    "keywords": "Plone 6, Reference Guide, Make Commands, Cookieplone"
---

# 🍪 Cookieplone Make Commands

This page provides a reference guide for all `make` commands used in Cookieplone.

## 🖥️ Frontend Commands

- **`make frontend-install`** → Installs dependencies for the React frontend.  
- **`make frontend-start`** → Starts the frontend development server.  
- **`make frontend-build`** → Builds the React frontend for production.  
- **`make frontend-test`** → Runs tests for the frontend.  

## ⚙️ Backend Commands

- **`make backend-install`** → Creates a virtual environment and installs Plone.  
- **`make backend-start`** → Starts the Plone backend server.  
- **`make backend-build`** → Builds the backend.  
- **`make backend-test`** → Runs tests on the backend.  
- **`make backend-create-site`** → Creates a new Plone site.  
- **`make backend-update-example-content`** → Exports example content.  

## 🐳 Docker Commands

- **`make stack-start`** → Starts all services (Frontend + Backend) using Docker.  
- **`make stack-stop`** → Stops all running services.  
- **`make stack-status`** → Checks service status.  
- **`make stack-create-site`** → Creates a new Plone site in Docker.  
- **`make stack-rm`** → Removes all services and volumes.  
- **`make build-images`** → Builds Docker images for the project.  

## 🛠️ Utility Commands

- **`make install`** → Runs both `backend-install` and `frontend-install`.  
- **`make start`** → Starts the entire project.  
- **`make test`** → Runs tests for both frontend and backend.  
- **`make check`** → Formats and lints the entire codebase.  
- **`make clean`** → Cleans temp files.  
- **`make help`** → Shows available commands.  

---

### **📌 Notes**
- Run **`make install`** before any `start` command to avoid missing dependencies.  
- If using Docker, **use `make stack-start`** instead of manually starting frontend and backend.  

📌 **Tip:** If you're unsure about a command, run `make help` to list all options.

---

### **🚀 Next Steps**
Rebuild with:
```sh
make html