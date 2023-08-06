import platform

import undetected_chromedriver as uc
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import read_version_from_cmd, PATTERN


PLATFORM = platform.system()
BRAVE_EXECUTABLE = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"


def set_up_driver(undetected: bool = False) -> Chrome | uc.Chrome:
    options = ChromeOptions()
    if PLATFORM != "Windows":
        version = read_version_from_cmd(
            f'"{BRAVE_EXECUTABLE}" --version', PATTERN["brave-browser"])
        driver_binary = ChromeDriverManager(version=version).install()
        options.binary_location = BRAVE_EXECUTABLE
        executable_path = BRAVE_EXECUTABLE
    else:
        driver_binary = ChromeDriverManager().install()
        executable_path = None
    if not undetected:
        return Chrome(service=Service(driver_binary), options=options)
    return uc.Chrome(
        driver_executable_path=driver_binary,
        browser_executable_path=executable_path)
