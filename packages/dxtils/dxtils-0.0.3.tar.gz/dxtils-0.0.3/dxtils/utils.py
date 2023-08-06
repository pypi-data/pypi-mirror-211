import platform

import requests as rq
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import read_version_from_cmd, PATTERN


PLATFORM = platform.system()
BRAVE_EXECUTABLE = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
CHROMEDRIVERS_URL = "https://chromedriver.chromium.org/downloads"


def get_sub_version(major_version: str) -> str:
    soup = BeautifulSoup(rq.get(CHROMEDRIVERS_URL).text, "html.parser")
    prefix = f"ChromeDriver {major_version}"
    text = soup.find(text=lambda t: t and t.startswith(prefix))
    return text.split()[1].strip()


def set_up_driver(
    undetected: bool = False, kwargs_only: bool = False
) -> Chrome | uc.Chrome | dict:
    options = ChromeOptions()
    if PLATFORM != "Windows":
        version = read_version_from_cmd(
            f'"{BRAVE_EXECUTABLE}" --version', PATTERN["brave-browser"])
        version = get_sub_version(version)
        driver_binary = ChromeDriverManager(version=version).install()
        options.binary_location = BRAVE_EXECUTABLE
        executable_path = BRAVE_EXECUTABLE
    else:
        driver_binary = ChromeDriverManager().install()
        executable_path = None        
    if not undetected:
        if kwargs_only:
            return {"service": Service(driver_binary), "options": options}
        return Chrome(service=Service(driver_binary), options=options)
    if kwargs_only:
        return {
            "driver_executable_path": driver_binary,
            "browser_executable_path": executable_path
        }
    return uc.Chrome(
        driver_executable_path=driver_binary,
        browser_executable_path=executable_path)
