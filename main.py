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
        url = f"{baseurl}/{category}/{region}"
        urls.append(url)
    return urls

def main():
    categories = get_categories()
    region = "trójmiasto"
    baseurl = "https://panoramafirm.pl/"
    urls = generate_urls(categories, region, baseurl)
    print(urls)

if __name__ == '__main__':
    main()