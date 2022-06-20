import os
import sys
from turtle import clear
import pandas as pd
import time
from selenium import webdriver

Url_politics = "https://www.aljazeera.net/news/politics/"
Url_business = "https://www.aljazeera.net/ebusiness/"
Url_curlture = "https://www.aljazeera.net/news/cultureandart/"
Url_science = "https://www.aljazeera.net/news/scienceandtechnology/"

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

## 4 - Science
Url = Url_science

driver.get(Url)


class scrap_AlJazeera:

    def __init__(self, driver=driver, url=Url):
        self.url = Url
        self.driver = driver
        self.articles = None

    def get_article_links(self):
        # Load Article Pages
        SCROLL_TIME_SLEEP = 3
        for _ in range(60):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.driver.find_element_by_xpath('//*[@id="news-feed-container"]/button').click()
            except Exception as e:
                break
            time.sleep(SCROLL_TIME_SLEEP)

        # Get Featured Articles Links
        link_elmts_featured = self.driver.find_elements_by_xpath('//*[@class="featured-articles-list__item"]/article[1]/div[2]/div[1]/h3[1]/a[1]')
        links_featured = [el.get_attribute("href") for el in link_elmts_featured]

        # Get Core Articles Links
        link_elmts_core = self.driver.find_elements_by_xpath('//*[@id="news-feed-container"]/article/div[2]/div[1]/h3[1]/a[1]')
        links_core = [el.get_attribute("href") for el in link_elmts_core]

        links_featured.extend(links_core)

        return links_featured

    def get_page_content(self,link):
        """
        Get a page link and return the text content as a list of Strings
        """
        driver.get(link)
        try:
            content_text = [self.driver.find_element_by_xpath('//*[@id="main-content-area"]/header[1]/h1[1]').text]
        except Exception as e:
            pass
            content_text = ['\n']
            print('Title Not found')

        content_elemt = self.driver.find_elements_by_xpath('//*[@id="main-content-area"]/div[2]/p')
        text = ['\n\n']
        for p in content_elemt:
            text.append(p.text)

        content_text.extend(text)
        # print(text)
        return content_text

    def get__pages_content(self):
        links = self.get_article_links()
        print(links)
        print(f"\n\nNumber of links = {len(links)}\n")

        for i, link in enumerate(links):
            content_text = self.get_page_content(link)
            string = ' '.join([str(item) for item in content_text])

            #open text file depending of the chosen topic
            # text_file = open(f"../raw_data/jazeera/politics/{i}.txt", "w", encoding='utf-8')
            # text_file = open(f"../raw_data/jazeera/culture/{i}.txt", "w", encoding='utf-8')
            # text_file = open(f"../raw_data/jazeera/economy/{i}.txt", "w", encoding='utf-8')
            text_file = open(f"../raw_data/jazeera/science/{i}.txt", "w", encoding='utf-8')


            #write string to file
            text_file.write(string)
            #close file
            text_file.close()





def main():
    scrapper = scrap_AlJazeera()
    scrapper.get__pages_content()


if __name__ == "__main__":
    main()
