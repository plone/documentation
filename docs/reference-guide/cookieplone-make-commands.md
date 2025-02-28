# CookiePlone Make Commands

This page provides a reference guide for all `make` commands used in CookiePlone.

## Frontend Commands

- **`make frontend-install`**  
  Installs all dependencies required for the React frontend.

- **`make frontend-start`**  
  Starts the frontend development server.

- **`make frontend-build`**  
  Builds the React frontend for production.

- **`make frontend-test`**  
  Runs tests for the frontend codebase.

## Backend Commands

- **`make backend-install`**  
  Creates a Python virtual environment and installs Plone.

- **`make backend-start`**  
  Starts the Plone backend server.

- **`make backend-build`**  
  Builds the backend.

- **`make backend-test`**  
  Runs tests on the backend codebase.

- **`make backend-create-site`**  
  Creates a new Plone site with default content.

- **`make backend-update-example-content`**  
  Exports example content inside the package.

## Docker Commands

- **`make stack-start`**  
  Starts all services (frontend + backend) using Docker.

- **`make stack-stop`**  
  Stops all running services.

- **`make stack-status`**  
  Checks the status of running services.

- **`make stack-create-site`**  
  Creates a new Plone site within the local stack.

- **`make stack-rm`**  
  Removes all services and volumes.

- **`make build-images`**  
  Builds Docker images for the project.

- **`make acceptance-containers-start`**  
  Starts the acceptance testing containers.

- **`make acceptance-containers-stop`**  
  Stops the acceptance testing containers.

- **`make acceptance-images-build`**  
  Builds acceptance testing frontend/backend images.

## Miscellaneous Commands

- **`make install`**  
  Runs both `backend-install` and `frontend-install`.

- **`make start`**  
  Starts the entire project.

- **`make test`**  
  Runs tests for both the frontend and backend.

- **`make check`**  
  Formats and lints the entire codebase.

- **`make clean`**  
  Cleans the installation by removing temporary files.

- **`make help`**  
  Displays a help message with all available commands.

## Notes

- Run **`make install`** before any `start` command to avoid missing dependencies.
- If using Docker, **prefer `make stack-start`** instead of manually starting frontend and backend.

## Tip

If you're unsure about a command, run `make help` to see all available options.
