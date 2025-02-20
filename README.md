# best-of-appium

best-of-appium "boppium" is [appium/python-client](https://github.com/appium/python-client) application code that has worked for me, for your reference.

## Execution report

A report of an execution captures:
1. What is controlled by appium (emulator specs metadata or real device connection configs)
2. Appium client code release tag
3. Test suite results

### Emulator
?? android studio export

## Example config files
### pytest
```python
# test/conftest.py
import pytest

import os, sys
sys.path.append(os.path.abspath("../best-of-appium"))
import boppium

@pytest.fixture
def android_driver_fn():
    return boppium.android_driver

# Custom pytest flag --no-skip for cases that are naturally skipped, because modifying the
# script is prone to accidental commits. See project Makefile for examples.
#
# https://docs.pytest.org/en/latest/reference/reference.html#pytest.hookspec.pytest_addoption {
from typing import Any, List
from typing_extensions import Final

NO_SKIP_OPTION: Final[str] = "--no-skip"

def pytest_addoption(parser):
    parser.addoption(NO_SKIP_OPTION, action="store_true", default=False, help="also run skipped tests")

def pytest_collection_modifyitems(config,
                                  items: List[Any]):
    if config.getoption(NO_SKIP_OPTION):
        for test in items:
            test.own_markers = [marker for marker in test.own_markers if marker.name not in ('skip', 'skipif')]
# }
```
### WSL notes

You actually can get your appium scripts working on Windows WSL with non-default network settings.
The following config is required, but in theory could bork your other projects.

```
# /mnt/c/Users/<UserName>/.wslconfig
[wsl2]  # https://learn.microsoft.com/en-us/windows/wsl/wsl-config
networkingMode=mirrored

[experimental]
hostAddressLoopback=true
```

### Native Windows notes

These conservative strategies might save you time down the road.
- Use current, non-preview, non-legacy version of PowerShell.
- Do whatever is recommended in Microsoft's documentation on setting up Node.js https://learn.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-windows.
- For appium client, use whatever's most recently updated by the appium team. At the time of writing it's dotnet.
    - Non-preview version of Visual Studio is as safe as it can get for programming dotnet scripts https://learn.microsoft.com/en-us/dotnet/core/install/windows#install-with-visual-studio.
- Use windows runner in Github Actions.  

## Usage

This repo is not a python package project; boppium is not intended to be installed.

```python
# Requiring boppium
import os, sys
sys.path.append(os.path.abspath("../best-of-appium"))


# test/conftest.py
import pytest, boppium

@pytest.fixture
def android_driver_fn():
    return boppium.android_driver


# test/example.py
def test_launch_logout(android_driver_fn):
    settings = {  # https://github.com/appium/appium-uiautomator2-driver
        'appium:app': STAGING_APK,
        'fullReset': False,
        'dontStopAppOnReset': True,
        'skipDeviceInitialization': True,
        'skipServerInstallation': True
    }

    with android_driver_fn(settings) as d:
        d.click('com.android.permissioncontroller:id/permission_allow_foreground_only_button')
        # ...
```

Acknowledgments
- https://stackoverflow.com/a/72437511
