import pytest

from app.data.plans import plans


# -------------------------
# Basic page routes
# -------------------------

PAGES = [
    "/",
    "/signup",
    "/plans",
    "/support",
    "/check-coverage",
    "/faq",
    "/apps",
    "/privacy",
    "/terms",
    "/contact",
    "/compatible-devices",
    "/thank-you",
]


@pytest.mark.parametrize("url", PAGES)
def test_pages_return_200(client, url):
    response = client.get(url)
    assert response.status_code == 200


# -------------------------
# Signup page
# -------------------------

def test_signup_page_with_plan_and_rental(client):
    plan_title = plans[0]["title"]

    response = client.get(
        "/signup",
        params={"plan": plan_title, "rental": 1},
    )

    assert response.status_code == 200
    assert plan_title in response.text


# -------------------------
# Submit signup
# -------------------------

def test_submit_signup_success(client):
    response = client.post(
        "/submit-signup",
        data={
            "full_name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "12345678",
            "address": "123 Main St",
            "city": "Townsville",
            "postal_code": "12345",
            "plan": plans[0]["title"],
            "rental": 1,
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"].endswith("/thank-you")


def test_submit_signup_invalid_form(client):
    response = client.post("/submit-signup", data={})
    assert response.status_code == 400


def test_submit_signup_honeypot_rejected(client):
    response = client.post(
        "/submit-signup",
        data={
            "full_name": "Spammer",
            "email": "spam@example.com",
            "phone": "12345678",
            "address": "123 Fake St",
            "city": "Nowhere",
            "postal_code": "12345",
            "plan": plans[0]["title"],
            "rental": 0,
            "company": "I am a bot",
        },
    )

    assert response.status_code == 400


def test_submit_signup_invalid_plan(client):
    response = client.post(
        "/submit-signup",
        data={
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone": "12345678",
            "address": "123 Main St",
            "city": "Townsville",
            "postal_code": "12345",
            "plan": "Totally Fake Plan",
            "rental": 0,
        },
    )

    assert response.status_code == 400


# -------------------------
# Submit contact
# -------------------------

def test_submit_contact_success(client):
    response = client.post(
        "/submit-contact",
        data={
            "name": "Alice",
            "email": "alice@example.com",
            "message": "I need help with my service",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert "success=1" in response.headers["location"]


def test_submit_contact_invalid_form(client):
    response = client.post("/submit-contact", data={})
    assert response.status_code == 400


def test_submit_contact_honeypot_rejected(client):
    response = client.post(
        "/submit-contact",
        data={
            "name": "Bot",
            "email": "bot@example.com",
            "message": "Spam message",
            "company": "spam",
        },
    )

    assert response.status_code == 400
