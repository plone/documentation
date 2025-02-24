---
myst:
  html_meta:
    "description": "Guide on managing users and groups in Plone."
    "property=og:description": "Learn how to create, manage, and assign roles to users and groups in Plone."
    "property=og:title": "Plone Users and Groups Management Guide"
    "keywords": "Plone, Users, Groups, Permissions, Roles, Plone 6"
---

# Users and Groups in Plone

Plone provides a robust user management system, allowing administrators to create and manage users, assign roles, and define permissions.

## **1. Managing Users**

You can manage users in the **Users and Groups** section of the Plone Control Panel.

### **Adding a New User**

1. Navigate to **Site Setup** → **Users and Groups**.
2. Click **Add new user** and fill in the details:
   - **Username**
   - **Email Address**
   - **Password**
3. Assign roles (e.g., **Member, Site Administrator, Manager**).
4. Click **Register** to create the user.

### **Editing and Deleting Users**

- Find the user in the **Users and Groups** section.
- Click **Edit** to update user details.
- Click **Delete** to remove the user from the system.

## **2. Managing Groups**

Groups allow administrators to assign roles to multiple users at once.

### **Creating a New Group**

1. Go to **Site Setup** → **Users and Groups** → **Groups**.
2. Click **Add new group**.
3. Enter the **Group Name** and an optional description.
4. Assign roles to the group (e.g., **Editor, Contributor**).
5. Click **Save**.

### **Adding Users to a Group**

1. Open the **Users and Groups** section.
2. Select a group and click **Manage members**.
3. Search for users and add them to the group.

## **3. Assigning Roles and Permissions**

Plone uses a role-based access control (RBAC) system. The main roles are:

- **Member** – Regular user with basic site access.
- **Editor** – Can edit and publish content.
- **Reviewer** – Can approve and publish content.
- **Manager** – Has full administrative access.

To change roles:

1. Navigate to **Users and Groups**.
2. Select a user or group.
3. Assign or modify roles using the **Roles** section.

## **4. Troubleshooting User and Group Issues**

- Ensure the correct permissions are assigned to users.
- Verify group roles if a user cannot access certain features.
- Check Plone logs for authentication errors.

```{todo}
Contribute to this documentation!
See issue [Backend > Users and Groups needs updates](https://github.com/plone/documentation/issues/1410).
```
