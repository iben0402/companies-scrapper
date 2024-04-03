import time
from selenium.webdriver.common.by import By
import os
from selenium import webdriver
import pandas as pd
import openpyxl

class Company:
    def __init__(self, name, phone, email, location, site):
        self.name = name
        self.phone = phone
        self.email = email
        self.location = location
        self.website = site
    def to_csv(self):
        return f"{self.name}|{self.phone}|{self.email}|{self.location}|{self.website}"

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
    driver.get(url)
    time.sleep(3)
    pagination_last_elements = driver.find_elements(By.CLASS_NAME, 'pagination-last')
    if pagination_last_elements:
        button = pagination_last_elements[0]
        a_element = button.find_elements(By.CSS_SELECTOR, 'a')

        if a_element:
            number_of_pages = a_element[0].get_attribute("data-paginatorpage")
            return int(number_of_pages)

    return 1


def open_page(driver, url):
    driver.get(url)
    time.sleep(2)
    companies = []
    company_cards = driver.find_elements(By.CLASS_NAME, 'company-item')
    for company in company_cards:
        name = company.find_element(By.CLASS_NAME, 'company-name').text
        address = company.find_element(By.CLASS_NAME, 'address').text
        phone = company.find_element(By.CLASS_NAME, 'icon-telephone').get_attribute("data-original-title")
        website = company.find_element(By.CLASS_NAME, 'icon-website').get_attribute("href")
        email = company.find_element(By.CLASS_NAME, 'icon-envelope').get_attribute("data-company-email")
        company = Company(name, phone, email, address, website)
        companies.append(company)

    return companies

def open_category(driver, url):
    print(f"opening {url}")
    num_of_pages = get_number_of_pages(driver, url)
    print(f"number of pages: {num_of_pages}")
    companies = []
    for i in range(1, num_of_pages+1):
        page_url = url+f"/firmy,{i}.html"
        companies += open_page(driver, page_url)
    return companies


def save_to_csv(companies, filename):
    folder = "data"
    print(f"saving to {folder}/{filename}")

    if not os.path.exists(folder):
        os.makedirs(folder)

    filepath = os.path.join(folder, filename)

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write("sep=|\n")

        for company in companies:
            file.write(company.to_csv() + "\n")

def save_to_excel(companies, filename):
    folder = "data"
    print(f"saving to {folder}/{filename}")

    if not os.path.exists(folder):
        os.makedirs(folder)

    filepath = os.path.join(folder, filename + ".xlsx")
    data = {
        "Name": [company.name for company in companies],
        "Phone": [company.phone for company in companies],
        "Email": [company.email for company in companies],
        "Location": [company.location for company in companies],
        "Website": [company.website for company in companies]
    }
    df = pd.DataFrame(data)
    df.to_excel(filepath, index=False)

def main():
    # SETUP
    categories = get_categories()
    region = "trójmiasto"
    baseurl = "https://panoramafirm.pl/"
    urls = generate_urls(categories, region, baseurl)
    driver = webdriver.Chrome()

    # OPEN CATEGORIES PAGES
    i = 0
    for url in urls:
        companies = []
        companies = open_category(driver, url)
        filename = categories[i].replace(" ", "_")
        # save_to_csv(companies, f"{filename}.csv")
        save_to_excel(companies, filename)
        i += 1

    driver.quit()


if __name__ == '__main__':
    main()
