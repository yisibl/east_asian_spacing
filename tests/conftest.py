import os
import sys
from pathlib import Path
import pytest

test_dir = Path(__file__).resolve().parent
sys.path.append(str(test_dir.parent))


@pytest.fixture(scope="session")
def data_dir():
    return test_dir / 'data'
