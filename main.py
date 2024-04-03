import time
from selenium.webdriver.common.by import By

from selenium import webdriver


def get_categories():
    categories = []
    with open('categories.txt', 'r', encoding='utf-8') as file:
        for line in file:
            categories.append(line.strip())
    return categories


def generate_urls(categories, region, baseurl):
    urls = []
    for category in categories:
        category_modified = category.replace(" ", "_")
        url = f"{baseurl}/{category_modified}/{region}"
        urls.append(url)
    return urls


def get_number_of_pages(driver, url):
    driver.get(self=driver, url=url)
    time.sleep(3)
    pagination_last_elements = driver.find_elements(By.CLASS_NAME, 'pagination-last')
    if pagination_last_elements:
        button = pagination_last_elements[0]
        a_element = button.find_elements(By.CSS_SELECTOR, 'a')
        if a_element:
            number_of_pages = a_element[0].find_elements(By.TAG_NAME, "data-paginatorpage")
            return number_of_pages

    return 1


def open_category(driver, url):
    print(f"opening {url}")
    num_of_pages = get_number_of_pages(driver, url)
    print(f"number of pages: {num_of_pages}")


def main():
    # SETUP
    categories = get_categories()
    region = "trójmiasto"
    baseurl = "https://panoramafirm.pl/"
    urls = generate_urls(categories, region, baseurl)
    driver = webdriver.Chrome()

    # OPEN CATEGORIES PAGES
    for url in urls:
        open_category(driver, url)

    driver.quit()


if __name__ == '__main__':
    main()
