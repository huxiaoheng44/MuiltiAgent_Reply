import os
import requests
from bs4 import BeautifulSoup

# 创建保存图片的文件夹
img_folder = "Img"
if not os.path.exists(img_folder):
    os.makedirs(img_folder)

# 要抓取的网页URL
url = "https://doc.meteonomiqs.com/doc/forecast.html#section/Response-Codes"

# 获取网页内容
response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to retrieve page, status code: {response.status_code}")
    exit()

# 解析网页内容
soup = BeautifulSoup(response.content, "html.parser")

# 查找所有img标签
img_tags = soup.find_all("img")

# 遍历所有img标签，检查是否为SVG图片
for img_tag in img_tags:
    img_url = img_tag.get("src")
    if img_url.endswith(".svg"):
        # 完整图片URL
        full_url = requests.compat.urljoin(url, img_url)
        
        # 获取图片的文件名
        img_name = os.path.basename(full_url)
        
        # 请求图片数据
        img_response = requests.get(full_url, stream=True)
        if img_response.status_code == 200:
            img_path = os.path.join(img_folder, img_name)
            # 保存图片到本地
            with open(img_path, "wb") as img_file:
                img_file.write(img_response.content)
            print(f"Downloaded {img_name} to {img_path}")
        else:
            print(f"Failed to download {full_url}, status code: {img_response.status_code}")
