import sys
from subprocess import run
from json import dumps as to_json
from urllib import parse
from os import makedirs, rmdir
from pathlib import Path

import pytest
import nc_py_install


APP_DATA_DIR = "./cloud_py_api"
TEST_CONFIG = {"loglvl": "DEBUG", "frmAppData": APP_DATA_DIR, "dbConfig": {}}

makedirs(Path(APP_DATA_DIR), exist_ok=True)


@pytest.mark.parametrize("action", ("--check", "--install", "--update", "--delete"))
def test__as_package_framework(action):
    print(TEST_CONFIG)
    test_config = parse.quote_plus(to_json(TEST_CONFIG, separators=(',', ':')))
    _result = run(
        [sys.executable, "-m", "nc_py_install", "--config", test_config, "--target", "framework", action], check=True
    )


rmdir(Path(APP_DATA_DIR))
