# pacman_ai/browser_control.py (Pyppeteer version)
import asyncio
import pyppeteer # pyppeteer-chromium-driver will be installed by pyppeteer

# URL for the Google Doodle Pac-Man game
PACMAN_URL = "https://www.google.com/logos/2010/pacman10-i.html"

async def launch_pacman_browser_pyppeteer():
    browser = None
    try:
        print("Attempting to launch browser with Pyppeteer...")
        # Pyppeteer will attempt to download Chromium if it's not found.
        # This download can be large and might cause timeouts in restricted environments.
        # args for compatibility, especially in Docker/headless environments
        browser = await pyppeteer.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        )
        page = await browser.new_page()

        print(f"Navigating to Pac-Man URL: {PACMAN_URL}")
        await page.goto(PACMAN_URL, timeout=60000) # 60s timeout for navigation
        print("Successfully navigated to Pac-Man page (Pyppeteer).")

        # Attempt to locate the game canvas
        try:
            # Wait for a canvas element to be present on the page
            await page.wait_for_selector("canvas", timeout=10000) # 10s timeout
            print("Canvas element found on the page (Pyppeteer).")
            # TODO: Get bounding box of the game canvas for screen capture.
            # TODO: Send keyboard inputs to this page or a specific element.
        except Exception as e:
            print(f"Could not find game canvas (Pyppeteer): {e}")

        print("Pac-Man browser setup complete (Pyppeteer).")
        # For testing, one might want to keep it open briefly if not headless,
        # but for automation, this will be handled differently.

    except Exception as e:
        print(f"An error occurred with Pyppeteer: {e}")
        # Check if error is related to Chromium download
        if "Chromium revision is not downloaded" in str(e) or "download_chromium" in str(e).lower():
            print("Pyppeteer error likely due to Chromium download issue or it not being found.")
            print("In some environments, Chromium needs to be pre-installed or pyppeteer.chromium_downloader.download_chromium() run manually.")
            print("Attempting to download Chromium with pyppeteer-install...")
            try:
                proc = await asyncio.create_subprocess_shell('pyppeteer-install')
                stdout, stderr = await proc.communicate()
                if proc.returncode == 0:
                    print("pyppeteer-install completed successfully. You might need to restart the script.")
                else:
                    print(f"pyppeteer-install failed. Stdout: {stdout.decode()}, Stderr: {stderr.decode()}")
            except Exception as install_e:
                print(f"Failed to run pyppeteer-install: {install_e}")

    finally:
        if browser:
            await browser.close()
        print("Browser closed (Pyppeteer).")

async def main():
    await launch_pacman_browser_pyppeteer()

if __name__ == "__main__":
    # Standard way to run asyncio main function
    # This handles environments like Jupyter where a loop might already be running.
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            print("Applied nest_asyncio for existing event loop (Pyppeteer).")
        loop.run_until_complete(main())
    except RuntimeError as e: # Fallback for some specific asyncio errors
        if "cannot schedule new futures after shutdown" in str(e):
            pass # Suppress common shutdown error if loop is finalizing
        else:
            raise
    print("Pyppeteer script finished.")
