"""Collection of unit tests and integration tests for the steamship client."""
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
VENV_PATH = ROOT_PATH / ".venv"
SRC_PATH = ROOT_PATH / "src"
TEST_ASSETS_PATH = ROOT_PATH / "test_assets"
APPS_PATH = Path(__file__).parent / "demo_apps"
