# Rebel Wireless Website

A fast, responsive website for **Rebel Wireless**, built with **FastAPI**, **Jinja2 templates**, **Tailwind CSS**, and **Flowbite**.  
Includes signup forms, a contact page, pricing plans, device compatibility listings, and interactive front-end features.

---

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Installation](#installation)  
- [Create and Activate Virtual Environment](#create-and-activate-virtual-environment)  
- [Running the Project](#running-the-project)  
- [Testing](#testing)  
- [Project Structure](#project-structure)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Features

- Dynamic landing page with hero, pricing, features, and testimonials sections  
- Signup form with server-side validation and Discord integration  
- Contact form with spam protection (honeypot)  
- Pricing page with rental toggle for plans  
- Support section with FAQ, coverage checker, and device compatibility  
- Interactive particles background on the homepage  
- Fully responsive navigation and footer  
- Accessible design using Tailwind CSS & Flowbite components  

---

## Tech Stack

- **Backend:** FastAPI, Starlette  
- **Templates:** Jinja2  
- **Frontend:** Tailwind CSS, Flowbite, JavaScript  
- **Form Validation:** Pydantic  
- **Testing:** Pytest, Pytest-asyncio  
- **Dev Tools:** Uvicorn ASGI server  
- **Integration:** Discord webhooks for form submissions  

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/rebelwireless/rebelwireless-website.git
cd rebelwireless-website

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install fastapi uvicorn jinja2 python-multipart pydantic aiofiles requests

### Running the Project
uvicorn app.main:app --reload

# Testing
pytest tests/

### License

This project is licensed under the MIT License. See LICENSE file for details.
