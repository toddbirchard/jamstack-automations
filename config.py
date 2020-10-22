"""Flask API configuration."""
import datetime
from os import environ, path

from dotenv import load_dotenv

# Load variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Flask API config from environment variables."""

    dt = datetime.datetime.today()

    # General Config
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"ssl": {"ca": "./creds/ca-certificate.crt"}}

    # Algolia API
    ALGOLIA_BASE_URL = environ.get("ALGOLIA_BASE_URL")
    ALGOLIA_APP_ID = environ.get("ALGOLIA_APP_ID")
    ALGOLIA_API_KEY = environ.get("ALGOLIA_API_KEY")

    # Google Cloud storage
    GCP_BUCKET_URL = environ.get("GCP_BUCKET_URL")
    GCP_BUCKET_NAME = environ.get("GCP_BUCKET_NAME")
    GOOGLE_APPLICATION_CREDENTIALS = path.join(basedir, "gcloud.json")
    GCP_BUCKET_FOLDER = [f'{dt.year}/{dt.strftime("%m")}']
    GCP_LYNX_DIRECTORY = "roundup"

    # Google BigQuery
    GCP_PROJECT = environ.get("GCP_PROJECT")
    GCP_BIGQUERY_TABLE = environ.get("GCP_BIGQUERY_TABLE")
    GCP_BIGQUERY_DATASET = environ.get("GCP_BIGQUERY_DATASET")
    GCP_BIGQUERY_URI = f"bigquery://{GCP_PROJECT}/{GCP_BIGQUERY_DATASET}"

    # Ghost
    GHOST_BASE_URL = environ.get("GHOST_BASE_URL")
    GHOST_ADMIN_API_URL = f"{GHOST_BASE_URL}/ghost/api/v3/admin"
    GHOST_API_USERNAME = environ.get("GHOST_API_USERNAME")
    GHOST_API_PASSWORD = environ.get("GHOST_API_PASSWORD")
    GHOST_CLIENT_ID = environ.get("GHOST_CLIENT_ID")
    GHOST_ADMIN_API_KEY = environ.get("GHOST_ADMIN_API_KEY")
    GHOST_API_EXPORT_URL = f"{GHOST_BASE_URL}/admin/db/"
    GHOST_NETLIFY_BUILD_HOOK = environ.get("GHOST_NETLIFY_BUILD_HOOK")

    # Mailgun
    MAILGUN_EMAIL_SERVER = environ.get("MAILGUN_EMAIL_SERVER")
    MAILGUN_EMAIL_TEMPLATE = environ.get("MAILGUN_EMAIL_TEMPLATE")
    MAILGUN_API_KEY = environ.get("MAILGUN_API_KEY")
    MAILGUN_FROM_SENDER = environ.get("MAILGUN_FROM_SENDER")
    MAILGUN_SUBJECT_LINE = "To Hack or to Slack; That is the Question."
    MAILGUN_PERSONAL_EMAIL = environ.get("MAILGUN_PERSONAL_EMAIL")

    # Mixpanel
    MIXPANEL_API_TOKEN = environ.get("MIXPANEL_API_TOKEN")

    # Twilio
    TWILIO_SENDER_PHONE = environ.get("TWILIO_SENDER_PHONE")
    TWILIO_RECIPIENT_PHONE = environ.get("TWILIO_RECIPIENT_PHONE")
    TWILIO_AUTH_TOKEN = environ.get("TWILIO_AUTH_TOKEN")
    TWILIO_ACCOUNT_SID = environ.get("TWILIO_ACCOUNT_SID")

    # Datadog
    DATADOG_TRACE_ENABLED = environ.get("DATADOG_TRACE_ENABLED")
    DATADOG_API_KEY = environ.get("DATADOG_API_KEY")
    DATADOG_APP_KEY = environ.get("DATADOG_APP_KEY")
