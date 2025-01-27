import os
import sys
import time
from urllib.parse import urlparse
from pandas import read_excel

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parser import parse_links, write_links


def get_filename_from_url(url):
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path)

def wait_for_file(file_path, check_interval=1):
    previous_size = -1
    while True:
        if os.path.exists(file_path):
            current_size = os.path.getsize(file_path)
            if current_size == previous_size:
                break
            previous_size = current_size
            time.sleep(check_interval)

def download_document(url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")  # Run headless Chrome
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode
    chrome_options.add_argument("--remote-debugging-port=9222")

    # Initialize the driver
    download_dir = os.getcwd()
    prefs = {
        "download.default_directory": download_dir,  # Set your custom download directory
        "download.prompt_for_download": False,  # Disable the prompt for download
        "download.directory_upgrade": True
    }

    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the page
    driver.get(url)

    try:
        # Wait for the dynamically loaded content to appear
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'article'))
        )

        link = driver.find_element(By.PARTIAL_LINK_TEXT, "Перечень организаций, формирований, индивидуальных предпринимателей")

        # Scrape link
        file_url = link.get_attribute('href')
        print(f"Загрузка с {file_url}")
        document = get_filename_from_url(file_url)
        filename = os.path.join(download_dir, document)
        if os.path.exists(filename):
            os.remove(filename)
        driver.get(file_url)
        wait_for_file(filename)
        print("Файл загружен")
        return filename

    finally:
        # Close the browser
        driver.quit()

def main() -> None:
    # Стартуем приложение
    url=sys.argv[1]
    if not url.endswith(".xlsx"):
        print(f"Навигация на страницу {url}")

        # Загружаем документ из приложения
        file = download_document(url)
    else:
        file = url
    df = read_excel(file)
    links = parse_links(df)
    download_dir = os.getcwd()
    output_file = os.path.join(download_dir, "output.xlsx")
    write_links(links, output_file)


if __name__ == "__main__":
    main()