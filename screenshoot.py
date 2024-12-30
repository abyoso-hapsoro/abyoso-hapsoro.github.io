import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


if __name__ == '__main__':
    # Set HTML path
    html_path = "docs/notes.html"

    # Set browser options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")

    # Start browser session
    browser = webdriver.Chrome(options=options)

    # Render HTML file
    browser.get(f"file://{os.path.abspath(html_path)}")
    browser.execute_script("document.body.style.zoom='150%'")

    # Take a screenshot of the rendered page
    browser.save_screenshot('screenshot.png')

    # Close the browser
    browser.quit()
