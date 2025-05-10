# AI-Generated Test for: Validate example in title for www.example.com
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def browser():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_validate_example_in_title(browser):
    browser.get("http://www.example.com")
    assert "Example Domain" in browser.title