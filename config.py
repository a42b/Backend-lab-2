import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    # General Flask settings
    PROPAGATE_EXCEPTIONS = True
    FLASK_DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

