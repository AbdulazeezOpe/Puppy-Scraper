
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import re
import os


def start_driver():
    options = webdriver.ChromeOptions()
     # ✅ Required for headless on Render
    
    chrome_bin = os.getenv("GOOGLE_CHROME_BIN", "/opt/render/project/.chrome/chrome/chrome")
    options.binary_location = chrome_bin

    
    options.add_argument("--headless=new")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.188 Safari/537.36')


    driver = uc.Chrome(options=options)
    #driver.maximize_window()
    return driver


def login(driver, email, password):
    driver.get('https://puppies.com/sign-in')
    time.sleep(5)

    if "403 Forbidden" in driver.page_source:
        print(f"🚫 403 Forbidden at {driver.current_url}")
        return None  # or handle as needed

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Accept']"))).click()

    time.sleep(3)
    driver.find_element(By.XPATH, "//input[@type='email' and @name='email']").send_keys(email)
    driver.find_element(By.XPATH, "//input[@type='password' and @name='password']").send_keys(password)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="sign-in-form"]/div/button').click()


def apply_filters(driver, city):
    wait = WebDriverWait(driver, 10)

    # Open Advanced Search and set age range
    adv_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Advanced Search']]")))
    adv_button.click()
    time.sleep(7)

    handles = driver.find_elements(By.CLASS_NAME, "rc-slider-handle")
    actions = ActionChains(driver)
    actions.click_and_hold(handles[0]).move_by_offset(20, 0).release().perform()  # Min age
    actions.click_and_hold(handles[1]).move_by_offset(-260, 0).release().perform()  # Max age
    time.sleep(2)
    adv_button.click()

    # City selection
    location_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "search_by")))
    location_dropdown.click()
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.react-select__option")))
    for option in driver.find_elements(By.CSS_SELECTOR, "div.react-select__option"):
        if "Search by City" in option.text:
            option.click()
            break

    city_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Type a city']")))
    city_input.clear()
    city_input.send_keys(city)
    time.sleep(3)
    city_input.send_keys(Keys.ENTER)

    # Radius
    distance_box = wait.until(EC.element_to_be_clickable((By.ID, "distance")))
    distance_box.click()
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.react-select__option")))
    for option in driver.find_elements(By.CSS_SELECTOR, "div.react-select__option"):
        if "100 mi" in option.text:
            option.click()
            break

    driver.find_element(By.XPATH, '//*[@id="search-listings-form"]/div/div/div[6]/div/button').click()


def get_listing_links(driver):
    listing_links = []
    page_number = 1

    def scrape_links_on_page():
        nonlocal listing_links
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/listings/"]')))
        anchors = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/listings/"]')
        for a in anchors:
            href = a.get_attribute("href")
            if href and href not in listing_links:
                listing_links.append(href)

    while True:
        scrape_links_on_page()
        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label="Next page"]')))
            if next_button.get_attribute("aria-disabled") == "true":
                break
            next_button.click()
            page_number += 1
            time.sleep(5)
        except:
            break
    return listing_links


def extract_listing_info(driver, url):
    driver.get(url)
    time.sleep(6)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    name = driver.find_element(By.TAG_NAME, "h1").text.strip()
    info_block = driver.find_element(By.XPATH, '//div[@class= "n al am iv i iw ix iy"]')
    breed = info_block.find_element(By.XPATH, './/a[contains(@href, "/find-a-puppy/")]').text
    age_block = info_block.find_element(By.XPATH, './/div[contains(text(), "Born on")]').text
    age = age_block.split("-")[-1].strip()
    city = info_block.find_element(By.XPATH, './/a[contains(@href, "/find-a-puppy/") and contains(text(), ",")]').text.strip()

    try:
        phone = driver.find_element(By.XPATH, '//span[contains(text(), "(")]').text.strip()
    except:
        phone = None

    if not phone:
        try:
            desc = driver.find_element(By.CSS_SELECTOR, 'p[aria-label="Listing Description"]').text
            match = re.search(r'\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', desc)
            phone = match.group(0) if match else "Not found"
        except:
            phone = "Not found"

    return {
        'Name': name,
        'Breed': breed,
        'Age': age,
        'City': city,
        'Phone': phone,
        'Link': url
    }


def run_scraper(city, email, password, report_to=None):
    driver = start_driver()
    login(driver, email, password)

    # After login
    if report_to:
        report_to.write("✅ Logged in successfully.")
    time.sleep(3)
    apply_filters(driver, city)
    time.sleep(5)

    if report_to:
        report_to.info(f"🔎 Searching listings for {city}...")
    
    links = get_listing_links(driver)

    # After links are collected
    if report_to:
        report_to.success(f"🔗 Found {len(links)} listings. Scraping details now...")
    time.sleep(3)
    all_data = []
    for i, link in enumerate(links, 1):
        if report_to:
            report_to.write(f"🔎 Scraping listing {i}/{len(links)}...")

        try:
            data = extract_listing_info(driver, link)
            all_data.append(data)
        except Exception as e:
            print(f"Failed on {link}: {e}")
            continue
    if report_to:
        report_to.success(f"✅ Scraped {len(all_data)} listings. Ready to download!")

    df = pd.DataFrame(all_data)
    output_file = f"puppies_{city.replace(',', '').replace(' ', '_')}.csv"
    df.to_csv(output_file, index=False)
    driver.quit()
    return output_file













