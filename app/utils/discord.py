# app/utils/discord.py
import os
import requests

# Read from environment
SIGNUP_WEBHOOK_URL = os.getenv("DISCORD_SIGNUP_WEBHOOK_URL")
CONTACT_WEBHOOK_URL = os.getenv("DISCORD_CONTACT_WEBHOOK_URL")


def _post_to_discord(webhook_url: str, payload: dict):
    """Internal helper to safely send Discord webhooks."""
    if not webhook_url:
        print("⚠️ Discord webhook URL not set")
        return

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        if response.status_code != 204:
            print(
                "❌ Discord webhook error:",
                response.status_code,
                response.text
            )
    except Exception as e:
        print("❌ Discord webhook exception:", str(e))


def send_signup_to_discord(full_name, email, address, phone, plan, rental):
    """Send signup message to the SIGNUP webhook."""
    clean_address = " ".join(line.strip() for line in address.splitlines())
    rental_text = f"${rental} Rental" if rental > 0 else "BYOD"

    payload = {
        "embeds": [
            {
                "title": "📥 New Signup",
                "color": 0xdc2626,
                "fields": [
                    {"name": "Name", "value": full_name, "inline": True},
                    {"name": "Email", "value": email, "inline": True},
                    {"name": "Phone", "value": phone, "inline": True},
                    {"name": "Plan", "value": plan, "inline": True},
                    {"name": "Device", "value": rental_text, "inline": True},
                    {"name": "Address", "value": clean_address, "inline": False},
                ]
            }
        ]
    }

    _post_to_discord(SIGNUP_WEBHOOK_URL, payload)


def send_contact_to_discord(name: str, email: str, message: str):
    """Send contact message to the CONTACT webhook."""
    payload = {
        "embeds": [
            {
                "title": "📩 New Contact Message",
                "color": 0xdc2626,
                "fields": [
                    {"name": "Name", "value": name, "inline": True},
                    {"name": "Email", "value": email, "inline": True},
                    {"name": "Message", "value": message.strip() or "No message provided", "inline": False}
                ]
            }
        ]
    }

    _post_to_discord(CONTACT_WEBHOOK_URL, payload)
