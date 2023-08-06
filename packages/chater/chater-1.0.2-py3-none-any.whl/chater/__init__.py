import os

from chater.api import (
    Auth,
    Models,
    Billing,
    StreamCompletion
)

api_key = os.environ.get("OPENAI_API_KEY")
api_base = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1/")
api_type = os.environ.get("OPENAI_API_TYPE", "open_ai")

openai_email = os.environ.get("OPENAI_EMAIL")
openai_password = os.environ.get("OPENAI_PASSWORD")