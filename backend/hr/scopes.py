default_scopes = {
    "offices:view": "View my business's offices",
    "organization:view": "View my business's offices",
    "admin:view": "View admin dashboard",
}

approvable_scopes = {
    "offices:edit": "Edit my business's offices",
    "organization:edit": "Edit my business's offices",
    "admin:edit": "Edit admin dashboard",
}

scopes = {}
scopes.update(default_scopes)
scopes.update(approvable_scopes)
