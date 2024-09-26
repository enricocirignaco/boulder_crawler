import time
import os
import sys
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

PAGE_LOAD_DELAY = 1000
def init_crawler():
    # Start Playwright
    with sync_playwright() as p:
        # Launch Chromium in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Go to the login page of sportsnow
        page.goto('https://www.sportsnow.ch/users/sign_in?locale=de')

        # Input your credentials
        page.fill('input[id="user_email"]', os.getenv('EMAIL'))
        page.fill('input[id="user_password"]', os.getenv('PASSWORD'))
        page.click('input[value="Anmelden"]')

        # Wait for the page to load
        page.wait_for_load_state('load')
        page.wait_for_timeout(PAGE_LOAD_DELAY)
        # Get the full text content of the page
        page_content = page.content()

        # Check if the string "Enrico Cirignaco" is present in the page content
        if "Enrico Cirignaco" in page_content:
            print("Login successful!")
        else:
            print("Login Error")
            restart_script()

        # Navigate to the bouldering slot page
        page.goto('https://www.sportsnow.ch/go/bfh-hochschulsport?locale=de')

        # Optionally, check the page title to confirm the right page
        title = page.title()
        if "BFH Hochschulsport" in title:
            print("Navigated to the correct page!")
        else:
            print("Navigation Error")
            restart_script()
    
        try:
            # Loop through the next 4 weeks
            for i in range(4):
                # Crawl the bouldering slots
                crawl_buoldering_slots(page)
                # Navigate to the next week
                navigate_to_next_week(page)
        except Exception as e:
            print("An error occurred: ", e)
            restart_script()
        finally:
            # Close the browser only when breaking the loop
            if browser.is_connected():
                browser.close()
############################################################################
def navigate_to_next_week(page):
        # Wait for the <a> element that contains the <i> element with class "fa fa-chevron-right"
        next_link = page.query_selector('a:has(i.fa.fa-chevron-right)')
        # Click the <a> element if it is found
        if next_link:
            next_link.click()
            page.wait_for_load_state('load')
            page.wait_for_timeout(PAGE_LOAD_DELAY)
            # print("current url: ", page.url)
        else:
            print("Error: link not found.")
            restart_script()
############################################################################
def crawl_buoldering_slots(page):
    # Select all calendar entries
    calendar_entries = page.query_selector_all('.cal-entry')

    # Iterate through each entry
    for entry in calendar_entries:
        # Check if the entry contains the text "Bouldern"
        if "Bouldern" in entry.text_content():
            # Locate the "Buchen" button
            primary_button = entry.query_selector('a.btn-primary')  # Adjust the selector as needed
            # Check if the button has a valid href attribute
            if(primary_button):
                    print("Found 'Bouldern' entry, clicking 'Buchen' button.")
                    primary_button.click()  # Click the "Buchen" button
                    page.wait_for_load_state('load')
                    page.wait_for_timeout(PAGE_LOAD_DELAY)
                    reserve_slot(page)
            # else:
            #         print("Button is disabled")
############################################################################
def reserve_slot(page):
    primary_button = page.query_selector('a.btn-primary')  # Adjust the selector as needed
    # Check if the button has a valid href attribute
    if(primary_button):
        print("Found valid abo")
        primary_button.click()  # Click the "Buchen" button
        page.wait_for_load_state('load')
        page.wait_for_timeout(PAGE_LOAD_DELAY)
        # look for the button to confirm the reservation
        confirm_button = page.query_selector('button.btn-primary')
        confirm_button.click()
        print("Slot reserved!")
        page.wait_for_load_state('load')
        page.wait_for_timeout(PAGE_LOAD_DELAY)
        print(page.title())
    else:
        print("Error: no valid abo found")
        restart_script()
############################################################################
def restart_script():
    """Restart the current script."""
    print("Restarting the script...")
    os.execv(sys.executable, ['python'] + sys.argv)
############################################################################
if __name__ == "__main__":
    print("Boulder Crawler v1.0")
    # Load environment variables from the .env file
    load_dotenv()
    while True:
        init_crawler()
        print("Standby for 5 minutes...")
        time.sleep(300)
