import lxml

import pandas as pd

from IPython.display import display
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup as bs



def parseGem():
    URL = "https://gemotest.ru/kirov/catalog/"
    SHORTEN_URL = "https://gemotest.ru"
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)

    driver.get('chrome://settings/')
    driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.8);')
    driver.maximize_window()

    driver.get(URL)

    html = driver.page_source
    soup = bs(html, "lxml")

    data_frame_dict = {
        "global_section": [],
        "section": [],
        "name": [],
        "price": []
    }

    global_sections = soup.find_all("div", class_="h3")

    for global_section in global_sections:
        section_information = global_section.find_next_sibling()
        sections = section_information.find_all("div", class_="caption")
        for section in sections:
            link = section.find("a")['href']

            driver.get(SHORTEN_URL + link)

            section_html = driver.page_source
            small_soup = bs(section_html, "lxml")
            names = small_soup.find_all("div", class_="title")
            for name in names[6:-29]:
                name_holder = name.find_parent()
                price_holder = name_holder.find_next_sibling()
                price = price_holder.find("div", class_="price")

                if price is None:
                    price = price_holder.find("span", class_="price")

                if price is None:
                    continue

                data_frame_dict["global_section"].append(global_section.text.strip())
                data_frame_dict["section"].append(section.text.strip())
                data_frame_dict["name"].append(name.text.strip())
                data_frame_dict["price"].append(price.text.strip().replace("&nbsp", ""))

    data_frame = pd.DataFrame(data_frame_dict)
    driver.quit()
    return data_frame


parseGem()
