default_scopes = {
    "users:view-mine": "View my account information",
    "users:edit-mine": "Edit my account information",
    "roles:view": "View roles",
    "roles:edit": "Edit roles",
    "users:view": "View all user accounts",
    "users:edit": "Edit all user accounts",
    "tasks:view": "View tasks",
    "tasks:edit": "Edit tasks"
}

approvable_scopes = {
    "openid": "OpenID Connect scope",
    "roles:edit": "Edit roles"
}

scopes = {}
scopes.update(default_scopes)
scopes.update(approvable_scopes)



