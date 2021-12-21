import logging
import os
import shutil
from glob import glob
from pathlib import Path

import pytest

@pytest.fixture(scope="session")
def thing():
    pass
