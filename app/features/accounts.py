"""Reference implementation for APP-002: accounts and revocable JWT sessions."""

from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from starlette.concurrency import run_in_threadpool

from app import security
from app.schemas import LoginInput, PublicUser, SignupInput

router = APIRouter()
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parents[1] / "templates")
)


def account_page(
    request: Request, name: str, status_code: int = 200, **context
) -> Response:
    """Render forms with a token; never put passwords back into an HTML response."""
    carrier = Response()
    token = security.csrf_token(request, carrier)
    response = templates.TemplateResponse(
        request=request,
        name=name,
        context={"csrf_token": token, "error": "", "username": "", **context},
        status_code=status_code,
    )
    response.raw_headers.extend(
        (name, value) for name, value in carrier.raw_headers if name == b"set-cookie"
    )
    return response


async def _form_credentials(request: Request, model) -> SignupInput | LoginInput:
    form = await request.form(max_fields=4, max_files=0, max_part_size=2048)
    security.require_csrf(request, form.get("csrf_token"))
    if len(form.multi_items()) != len(form):
        raise HTTPException(422, "Submit each field once.")
    values = {key: value for key, value in form.items() if key != "csrf_token"}
    return model.model_validate(values)


@router.get("/api/csrf")
def api_csrf(request: Request, response: Response) -> dict[str, str]:
    """Same-origin clients get a pre-session without receiving an auth token."""
    response.headers["Cache-Control"] = "no-store"
    return {"csrf_token": security.csrf_token(request, response)}


@router.post("/api/signup", status_code=201, response_model=PublicUser)
def api_signup(request: Request, credentials: SignupInput) -> dict[str, str]:
    """Public signup cannot choose an administrator role."""
    security.require_csrf(request, request.headers.get("X-CSRF-Token"))
    security.limit_signup(request)
    return security.signup(
        request.app.state.settings, credentials.username, credentials.password
    )


@router.post("/api/login", response_model=PublicUser)
def api_login(
    request: Request, response: Response, credentials: LoginInput
) -> dict[str, str]:
    """A successful login sets an HttpOnly cookie, never a JSON bearer token."""
    security.require_csrf(request, request.headers.get("X-CSRF-Token"))
    return security.login(request, response, credentials.username, credentials.password)


@router.post("/api/logout")
def api_logout(request: Request, response: Response) -> dict[str, str]:
    """Revoke the server session as well as clearing the browser cookie."""
    security.require_csrf(request, request.headers.get("X-CSRF-Token"))
    security.logout(request, response)
    return {"message": "You are logged out."}


@router.get("/api/me", response_model=PublicUser)
def api_me(request: Request) -> dict[str, str]:
    """Current identity is derived from verified state, never browser role text."""
    return security.require_user(request)


@router.get("/signup")
def signup_page(request: Request) -> Response:
    """Start with a real form and an anonymous synchronizer token."""
    return account_page(request, "signup.html")


@router.get("/login")
def login_page(request: Request) -> Response:
    """Explain the next step after signup without automatically logging in."""
    return account_page(
        request, "login.html", created=request.query_params.get("created") == "1"
    )


@router.post("/signup")
async def signup_form(request: Request) -> Response:
    """Keep browser failures in the form where the student can recover."""
    credentials = None
    try:
        credentials = await _form_credentials(request, SignupInput)
        security.limit_signup(request)
        await run_in_threadpool(
            security.signup,
            request.app.state.settings,
            credentials.username,
            credentials.password,
        )
    except ValidationError:
        return account_page(
            request,
            "signup.html",
            status_code=422,
            error="Use a 3–32 character username and a 15–128 character passphrase.",
        )
    except HTTPException as error:
        return account_page(
            request,
            "signup.html",
            status_code=error.status_code,
            error=error.detail,
            username=credentials.username if credentials else "",
        )
    return RedirectResponse("/login?created=1", status_code=303)


@router.post("/login")
async def login_form(request: Request) -> Response:
    """Rotate the session only after CSRF and credentials have been checked."""
    response = RedirectResponse("/dashboard", status_code=303)
    credentials = None
    try:
        credentials = await _form_credentials(request, LoginInput)
        await run_in_threadpool(
            security.login,
            request,
            response,
            credentials.username,
            credentials.password,
        )
    except ValidationError:
        return account_page(
            request,
            "login.html",
            status_code=422,
            error="Enter your username and password.",
        )
    except HTTPException as error:
        return account_page(
            request,
            "login.html",
            status_code=error.status_code,
            error=error.detail,
            username=credentials.username if credentials else "",
        )
    return response


@router.post("/logout")
async def logout_form(request: Request) -> Response:
    """A link or GET request can never log someone out."""
    form = await request.form(max_fields=1, max_files=0, max_part_size=2048)
    security.require_csrf(request, form.get("csrf_token"))
    response = RedirectResponse("/", status_code=303)
    security.logout(request, response)
    return response


@router.get("/dashboard")
def dashboard(request: Request) -> Response:
    """The visible member page is protected by the same server check as the API."""
    user = security.authenticate(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)
    return account_page(request, "dashboard.html", user=user)
