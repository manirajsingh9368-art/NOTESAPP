

import os
from datetime import timedelta

# absolute path to project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATABASE_PATH = os.path.join(BASE_DIR, "Notes_v14.db")


class Config:

    DATABASE_PATH = DATABASE_PATH

    JWT_SECRET_KEY = "this-is-a-very-long-super-secure-secret-key-for-jwt-authentication"

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

    # JWT_TOKEN_LOCATION = ["cookies"]

    JWT_TOKEN_LOCATION = ["headers"]

    JWT_COOKIE_SECURE = False

    JWT_COOKIE_CSRF_PROTECT = False