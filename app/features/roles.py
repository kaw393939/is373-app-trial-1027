"""Reference implementation for APP-003: server-enforced member and admin roles."""

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app import security
from app.features.accounts import account_page

router = APIRouter()


@router.get("/api/admin")
def api_admin(request: Request) -> dict[str, str]:
    """Return no admin response unless the current database role grants access."""
    user = security.require_admin(request)
    return {"message": "Admin access granted.", "role": user["role"]}


@router.get("/admin")
def admin_page(request: Request):
    """Typing the URL directly cannot bypass permission checks."""
    user = security.authenticate(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)
    if user["role"] != "admin":
        return account_page(request, "access-denied.html", status_code=403, user=user)
    return account_page(request, "admin.html", user=user)
