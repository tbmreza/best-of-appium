# best-of-appium

best-of-appium "boppium" is [appium/python-client](https://github.com/appium/python-client) application code that has worked for me, for your reference.

## WSL notes

You actually can get your appium scripts working on Windows WSL with non-default network settings.
The following config is required, but in theory could bork your other projects.

```
# /mnt/c/Users/<UserName>/.wslconfig
[wsl2]  # https://learn.microsoft.com/en-us/windows/wsl/wsl-config
networkingMode=mirrored

[experimental]
hostAddressLoopback=true
```

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
