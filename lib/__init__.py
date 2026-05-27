"""Geek CLAUDE - UGC library. Auto-loads .env from project root."""
import os
from dotenv import load_dotenv

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(_ROOT, ".env"))
