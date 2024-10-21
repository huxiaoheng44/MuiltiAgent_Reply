import os
import requests
from bs4 import BeautifulSoup

a = "this is redundant"
img_folder = "Img"
if not os.path.exists(img_folder):
    os.makedirs(img_folder)


url = "https://doc.meteonomiqs.com/doc/forecast.html#section/Response-Codes"


response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to retrieve page, status code: {response.status_code}")
    exit()


soup = BeautifulSoup(response.content, "html.parser")


img_tags = soup.find_all("img")


for img_tag in img_tags:
    img_url = img_tag.get("src")
    if img_url.endswith(".svg"):

        full_url = requests.compat.urljoin(url, img_url)
        

        img_name = os.path.basename(full_url)
        

        img_response = requests.get(full_url, stream=True)
        if img_response.status_code == 200:
            img_path = os.path.join(img_folder, img_name)

            with open(img_path, "wb") as img_file:
                img_file.write(img_response.content)
            print(f"Downloaded {img_name} to {img_path}")
        else:
            print(f"Failed to download {full_url}, status code: {img_response.status_code}")
