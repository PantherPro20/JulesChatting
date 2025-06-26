# pacman_ai/playwright_control.py
import asyncio
from playwright.async_api import async_playwright, Playwright # type: ignore

# URL for the Google Doodle Pac-Man game
PACMAN_URL = "https://www.google.com/logos/2010/pacman10-i.html"
# Alternate URL if the above has issues embedding or with SSL in automated browsers
# PACMAN_URL_HTTP = "http://www.google.com/logos/pacman10-i.html"


async def launch_browser_and_navigate(p: Playwright, headless_mode=True):
    """
    Launches a browser using Playwright, navigates to the Pac-Man URL,
    and returns the page object.
    Note: Successful execution depends on the environment having necessary
    system libraries for the Playwright browsers (e.g., GTK, GLib, etc.).
    """
    browser = None
    page = None
    print(f"Attempting to launch browser (headless={headless_mode}) with Playwright...")

    try:
        # Try Chromium first
        browser = await p.chromium.launch(headless=headless_mode)
        # browser = await p.firefox.launch(headless=headless_mode) # Alternative
        # browser = await p.webkit.launch(headless=headless_mode) # Alternative

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            # viewport={"width": 800, "height": 600}, # Optional: set viewport size
            # ignore_https_errors=True # Optional: if facing SSL issues with the URL
        )
        page = await context.new_page()

        print(f"Navigating to Pac-Man URL: {PACMAN_URL}")
        await page.goto(PACMAN_URL, timeout=60000, wait_until='load') # wait_until can be 'domcontentloaded', 'load', or 'networkidle'
        print("Successfully navigated to Pac-Man page with Playwright.")

        # Placeholder for finding the game canvas - this will be crucial
        try:
            # The Google Doodle Pac-Man game is often within an iframe or specific div.
            # If it's in an iframe, you need to switch to the frame's content.
            # Example: game_iframe = page.frame(name="game") or page.frame_locator("#game")
            # if game_iframe:
            #     canvas_element = await game_iframe.query_selector("canvas")
            # else:
            #     canvas_element = await page.query_selector("canvas")

            # For the 2010 Pacman doodle, it might be simpler:
            # Try a few common selectors for canvas elements in order of likelihood for this page
            canvas_selectors = [
                "#hplogo canvas",      # Canvas within the main logo div (often used for doodles)
                "canvas#game",         # Canvas with id 'game'
                "canvas#pacman-canvas",# Canvas with id 'pacman-canvas'
                "canvas"               # Any canvas element as a fallback
            ]
            canvas_element = None
            for selector in canvas_selectors:
                canvas_element = await page.query_selector(selector)
                if canvas_element:
                    print(f"Canvas element found using selector: '{selector}'")
                    break

            if canvas_element:
                # bounding_box = await canvas_element.bounding_box()
                # if bounding_box:
                #     print(f"Canvas bounding box: {bounding_box}")
                pass # Further actions would go here
            else:
                print("Could not find game canvas using common selectors. Further interaction might fail.")
        except Exception as e:
            print(f"Error finding canvas: {e}")

        # Return page for further interaction. Browser should be closed by the caller.
        return page, browser # Return both to manage their lifecycle

    except Exception as e:
        print(f"An error occurred with Playwright browser launch or navigation: {e}")
        print("This might be due to missing host system libraries required by Playwright's browsers.")
        print("Run 'python -m playwright install --with-deps' locally to install system dependencies if possible,")
        print("or ensure your environment has GUI/graphics libraries (e.g., GTK, X11 libs).")
        if page:
            try:
                await page.close()
            except Exception as pe:
                print(f"Error closing page: {pe}")
        if browser:
            try:
                await browser.close()
            except Exception as be:
                print(f"Error closing browser: {be}")
        return None, None


async def example_usage():
    """Example of how to use launch_browser_and_navigate."""
    async with async_playwright() as p:
        page, browser = await launch_browser_and_navigate(p, headless_mode=True)

        if page and browser:
            print("Page loaded. Performing a quick test action (getting title).")
            try:
                title = await page.title()
                print(f"Page title: {title}")

                # Example: Taking a screenshot (Playwright's own method)
                # await page.screenshot(path="playwright_pacman_screenshot.png")
                # print("Screenshot 'playwright_pacman_screenshot.png' taken.")
            except Exception as e:
                print(f"Error during page interaction (title/screenshot): {e}")
            finally:
                # Cleanly close browser
                await browser.close()
                print("Playwright browser closed after example usage.")
        else:
            print("Failed to launch browser or navigate with Playwright in example_usage.")

if __name__ == "__main__":
    print("Running Playwright Control Script Example...")
    # asyncio.run(example_usage())
    # Using get_event_loop().run_until_complete() for wider compatibility.
    loop = asyncio.get_event_loop()
    if loop.is_running():
        import nest_asyncio
        nest_asyncio.apply()
        print("Applied nest_asyncio for existing event loop (Playwright).")
    try:
        loop.run_until_complete(example_usage())
    except Exception as e:
        print(f"Error during example_usage execution: {e}")
    print("Playwright script example finished.")
