
import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError(
            "Missing SUPABASE_URL or SUPABASE_KEY in .env. "
            "Add both values before using Supabase."
        )

    return create_client(url, key)


supabase: Client | None = None


def get_client() -> Client:
    global supabase
    if supabase is None:
        supabase = get_supabase_client()
    return supabase
