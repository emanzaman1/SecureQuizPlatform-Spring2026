import sys
import os

# Add project root to Python path so CI can find app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


def test_app_exists():
    assert app is not None