import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


def _validate_input(
    html_path: str,
    target_path: str,
    window_size: str,
    zoom_level: int
) -> None:
    """
    Validate arguments passed to `html2image`
    """

    # Validate HTML path
    if not isinstance(html_path, str):
        raise TypeError(f"html_path must be string, got {type(html_path).__name__} instead.")
    if not os.path.isfile(html_path):
        raise FileNotFoundError(f"'{html_path}' not found. Please ensure the HTML path is correct.")
    
    # Validate target path then ensure its directory exists
    if not isinstance(target_path, str):
        raise TypeError(f"target_path must be string, got {type(target_path).__name__} instead.")
    target_dir = os.path.dirname(target_path)
    if target_dir and not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    
    # Validate window size
    if not isinstance(window_size, str):
        raise TypeError(f"window_size must be string, got {type(window_size).__name__} instead.")
    if ',' not in window_size:
        raise ValueError(f"window_size must contain a comma, e.g., '1920,1080'.")
    sizes = window_size.split(",")
    if len(sizes) != 2 or not all(size.isdigit() for size in sizes):
        raise ValueError(f"window_size must contain two integers separated by a comma, e.g., '1920,1080'.")
    
    # Validate zoom level
    if not isinstance(zoom_level, int):
        raise TypeError(f"zoom_level must be integer, got {type(zoom_level).__name__} instead.")
    if zoom_level <= 0:
        raise ValueError(f"zoom_level must be positive integer.")


def html2image(
    html_path: str,
    target_path: str,
    window_size: str = "1920,1080",
    zoom_level: int = 150
) -> None:
    """
    Renders HTML page then snaps a screenshot of that page.

    Args:
        html_path (str):
            Path to the HTML.
        target_path (str):
            Path to save the screenshot image.
        window_size (str):
            Browser window size for screenshot image. Defaults to "1920,1080".
        zoom_level (int):
            Page zoom level in percentage. Defaults to 150.
    """

    # Validate inputs
    args = [eval(arg) for arg in html2image.__code__.co_varnames[:html2image.__code__.co_argcount]]
    _validate_input(*args)

    # Set browser options
    options = Options()
    options.add_argument("--headless")
    options.add_argument(f"--window-size={window_size}")    

    try:
        # Start browser session
        browser = webdriver.Chrome(options=options)
        
        # Render HTML file
        browser.get(f"file://{os.path.abspath(html_path)}")
        browser.execute_script(f"document.body.style.zoom='{zoom_level}%'")

        # Take a screenshot of the rendered page
        browser.save_screenshot(target_path)
    
    except WebDriverException as e:
        # Handle browser-related exceptions
        raise RuntimeError(f"Webdriver error occurred: {e}")
    
    except Exception as e:
        # Raise other errors if any are encountered
        raise RuntimeError(f"An error occurred while processing the HTML: {e}")

    finally:
        # Close the browser
        browser.quit()


if __name__ == '__main__':
    # Screenshot the release notes
    html2image("docs/notes.html", "screenshot.png")
