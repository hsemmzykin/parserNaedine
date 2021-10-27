import requests as req
from bs4 import BeautifulSoup as bs
import lxml
import pandas as pd
import numpy as np

def createFrame():
    URL = "https://klinika-naedine.ru/prices"
    page = req.get(URL)
    soup = bs(page.text, "lxml")

    data_frame_dict = {
        "department": [],
        "med_section": [],
        "specialty": [],
        "service": [],
        "price": []
    }

    doctors = soup.find_all("span", class_="prices-page__category-name")
    for doctor in doctors:
        parent = doctor.find_parent()
        content_div = parent.find_next_sibling()
        services = content_div.find_all("div", class_="price-item__name price-item__text")

        for service in services:
            price = service.find_next_sibling().find("span", class_="price-item__price-value")

            r_doctor = doctor.text.strip()
            r_service = service.text.strip()
            r_price = price.text.strip()
            # 404, особые значения не учитываются при статистическом анализе
            data_frame_dict["department"].append(np.nan)
            data_frame_dict["med_section"].append(np.nan)


            # data 
            data_frame_dict["specialty"].append(r_doctor)
            data_frame_dict["service"].append(r_service)
            data_frame_dict["price"].append(r_price)

    data_frame = pd.DataFrame(data_frame_dict)
    compression_opts = dict(method='zip', archive_name='result.csv')
    data_frame.to_csv('result.zip', index=False, compression=compression_opts) 
if __name__ == '__main__':
    createFrame()

