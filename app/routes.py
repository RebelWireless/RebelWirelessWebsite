from typing import Optional, Set
from urllib.parse import unquote
import logging

from fastapi import (
    APIRouter,
    Request,
    HTTPException,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, EmailStr, constr, ValidationError

from app.data.plans import plans, disclaimers
from app.data.device_list import wisp_devices
from app.data.coverage import served_locations
from app.data.testimonials import testimonials
from app.utils.discord import (
    send_signup_to_discord,
    send_contact_to_discord,
)

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# -------------------------
# Helpers
# -------------------------

def render(request: Request, template: str, **context):
    """DRY helper for template rendering (Starlette-compatible)."""
    return templates.TemplateResponse(
        request,
        template,
        context,
    )


VALID_PLAN_TITLES: Set[str] = {p["title"] for p in plans}


# -------------------------
# Pydantic Form Models
# -------------------------

class SignupForm(BaseModel):
    full_name: constr(min_length=2)
    email: EmailStr
    phone: constr(min_length=7, max_length=20)
    address: constr(min_length=3)
    city: constr(min_length=2)
    postal_code: constr(min_length=4, max_length=10)
    plan: str
    rental: int
    company: Optional[str] = None  # honeypot


class ContactForm(BaseModel):
    name: constr(min_length=2)
    email: EmailStr
    message: constr(min_length=5)
    company: Optional[str] = None  # honeypot


# -------------------------
# Routes
# -------------------------

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return render(
        request,
        "index.html",
        plans=plans,
        disclaimers=disclaimers,
        testimonials=testimonials,
    )


@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request, plan: str = "", rental: int = 0):
    selected_plan = next(
        (p for p in plans if p["title"] == unquote(plan)),
        None,
    )
    return render(
        request,
        "signup.html",
        plan=selected_plan,
        rental=rental,
    )


@router.post("/submit-signup")
async def submit_signup(request: Request):
    form_data = await request.form()

    try:
        form = SignupForm(**form_data)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid form submission")

    # Honeypot spam protection
    if form.company:
        raise HTTPException(status_code=400)

    # Validate plan server-side
    if form.plan not in VALID_PLAN_TITLES:
        raise HTTPException(status_code=400, detail="Invalid plan selected")

    full_address = f"{form.address} {form.city} {form.postal_code}"

    # Non-blocking Discord call
    try:
        await run_in_threadpool(
            send_signup_to_discord,
            form.full_name,
            form.email,
            full_address,
            form.phone,
            form.plan,
            form.rental,
        )
    except Exception:
        logger.exception("Failed to send signup to Discord")

    return RedirectResponse(
        url=request.url_for("thank_you"),
        status_code=303,
    )


@router.get("/thank-you", response_class=HTMLResponse)
async def thank_you(request: Request):
    return render(request, "thank_you.html")


@router.get("/plans", response_class=HTMLResponse)
async def plans_page(request: Request):
    return render(
        request,
        "plans.html",
        plans=plans,
        disclaimers=disclaimers,
    )


@router.get("/support", response_class=HTMLResponse)
async def support(request: Request):
    return render(
        request,
        "support.html",
        locations=served_locations,
    )


@router.get("/check-coverage", response_class=HTMLResponse)
async def check_coverage(request: Request):
    return render(
        request,
        "check_coverage.html",
        locations=served_locations,
    )


@router.get("/faq", response_class=HTMLResponse)
async def faq(request: Request):
    return render(request, "faq.html")


@router.get("/apps", response_class=HTMLResponse)
async def apps(request: Request):
    return render(request, "apps.html")


@router.get("/privacy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    return render(request, "privacy.html")


@router.get("/terms", response_class=HTMLResponse)
async def terms_conditions(request: Request):
    return render(request, "terms.html")


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return render(request, "contact.html")


@router.post("/submit-contact")
async def submit_contact(request: Request):
    form_data = await request.form()

    try:
        form = ContactForm(**form_data)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid form submission")

    # Honeypot spam protection
    if form.company:
        raise HTTPException(status_code=400)

    try:
        await run_in_threadpool(
            send_contact_to_discord,
            form.name,
            form.email,
            form.message,
        )
    except Exception:
        logger.exception("Failed to send contact message to Discord")

    return RedirectResponse(
        url=request.url_for("contact").include_query_params(success=1),
        status_code=303,
    )


@router.get("/compatible-devices", response_class=HTMLResponse)
async def devices_page(request: Request):
    return render(
        request,
        "compatible-devices.html",
        devices=wisp_devices,
    )
