#coding:utf-8

import requests, re, os
import pandas as pd
from bs4 import BeautifulSoup

def download_img(img_url_list,title_name,author_name,url_start_number):

    try:
        file_path = "/Users/yang/Downloads/{0} - {1} - {2}".format(url_start_number,author_name,title_name)   # 获取下载路径

        if len(img_url_list) > 0 and not os.path.exists(file_path):  # 保证有照片爬取,且路径不存在
            os.mkdir(file_path)     # 创建文件夹
            x = 1
            for img_url in img_url_list:  # 依次迭代下载图片
                r = requests.get(img_url)
                with open("{0}/{1}.jpg".format(file_path, x), "wb") as f:  # 在文件夹中创建图片文件，以二进制写入
                    f.write(r.content)
                x += 1
            print("已爬{}张图片".format(len(img_url_list)))
        elif len(img_url_list) == 0:
            print("无照片可爬取")
        else:
            print("曾经爬取过")

    except Exception as e:
        print("保存出错", e)

def get_img_url(url_text,url_title,url_start_number):

    try:
        soup = BeautifulSoup(url_text, "html.parser")
        img_url_list_old = []   # 设定旧url空列表

        for img_addr in re.findall(r'file="(.+?)"', str(soup.find_all("img"))):  # 获取img标签中属性file的值，即为图片url中地址信息
            img_url_list_old.append(url_title + img_addr)   # 整合成完整的图片url，添加到url列表中

        # 获取url的title名和作者名
        title_name = re.findall(r"<title>(.+?) - ", str(soup.find_all("title")))[0]
        author_name = re.findall(r">(.+?)</a>", str(soup.find_all("div", attrs={"class": "postinfo"})))[0]

        # 旧url列表去重，且保持顺序不变
        img_url_list = list(set(img_url_list_old))
        img_url_list.sort(key = img_url_list_old.index)

        download_img(img_url_list,title_name,author_name,url_start_number)

    except Exception as e:
        print("图片链接获取失败", e)


def get_html(url,url_title,url_start_number):

    try:
        kw = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        r = requests.get(url,headers = kw,timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        url_text = r.text

        get_img_url(url_text,url_title,url_start_number)

    except Exception as e:
        print("爬取失败", e)

def get_url_list():

    try:
        df = pd.read_excel(r"/Users/yang/文件/000 - 资料/url/url.xlsx", sheet_name = 0)
        return df["real_url"][1656:1668], df["91_url"][0]

    except Exception as e:
        print("获取url失败", e)

def main():

    try:
        url_for_download, url_title = get_url_list()
        url_start_number = 1656
        for url in url_for_download:
            print(url_start_number, end = " ")
            get_html(url,url_title,url_start_number)
            url_start_number += 1

    except Exception as e:
        print(e,"\n主程序错误")

if __name__ == "__main__":
    main()




