import os
import sys
from turtle import clear
import pandas as pd
import time
from selenium import webdriver

Url_politics = "https://www.hespress.com/politique"
Url_business = "https://www.hespress.com/economie"
Url_curlture = "https://www.hespress.com/art-et-culture"
Url_tamazight = "https://www.hespress.com/tamazight"

opts = webdriver.ChromeOptions()
opts.headless = False
driver = webdriver.Chrome(
    executable_path="C:\\chromedriver\\chromedriver100.exe")

# Choose your topic
## 1 - Politics
# Url = Url_politics

## 2 - Culture
# Url = Url_curlture

## 3 - Business
# Url = Url_business

## 4 - Tamazight
Url = Url_tamazight

driver.get(Url)

class scrap_Hespress:

    def __init__(self, driver=driver, url=Url):
        self.url = Url
        self.driver = driver
        self.articles = None

    def get_article_links(self):
        for _ in range(100):
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        liks_elmt = self.driver.find_elements_by_xpath('//*[@id="listing"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/a[1]')
        # //*[@id="listing"]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/a[1]
        links_list = [el.get_attribute("href") for el in liks_elmt]
        print(links_list)
        print(f"Number of articles : {len(links_list)}")

        return links_list

    def get_page_content(self, link):
        """
        Get a page link and return the text content as a list of Strings
        """
        driver.get(link)
        content_text = [self.driver.find_element_by_xpath('//*[@class="post-title"]').text]
        print("TITLE:   ",content_text)
        paragraphs = self.driver.find_elements_by_xpath('//*[@class="article-content"]/p')
        text = ['\n\n']
        for p in paragraphs:
            text.append(p.text)

        content_text.extend(text)
        print(content_text)

        return content_text

    def get_pages_content(self):
        links = self.get_article_links()
        print(links)
        print(f"\n\nNumber of links = {len(links)}\n")

        for i, link in enumerate(links):
            content_text = self.get_page_content(link)
            string = ' '.join([str(item) for item in content_text])

            #open text file depending of the chosen topic
            # text_file = open(f"../raw_data/hespress/politics/{i}.txt", "w", encoding='utf-8')
            # text_file = open(f"../raw_data/hespress/culture/{i}.txt", "w", encoding='utf-8')
            # text_file = open(f"../raw_data/hespress/economy/{i}.txt","w",encoding='utf-8')
            text_file = open(f"../raw_data/hespress/tamazight/{i}.txt", "w", encoding='utf-8')


            #write string to file
            text_file.write(string)
            #close file
            text_file.close()




def main():
    scrapper = scrap_Hespress()
    scrapper.get_pages_content()


if __name__ == "__main__":
    main()
