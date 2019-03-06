# div class_= poster--->a["href"]---->add(imdb+a["href"])---->div[1] class_=pswp__zoom-wrap--->img[1]["src"]


from selenium import webdriver
from bs4 import BeautifulSoup
import requests

class Film :
    def __init__(self):
        self.rank = ""
        self.title = ""
        self.year = ""
        self.link = ""
def get_film_list():

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome("/home/rahul/Downloads/chromedriver_linux64/chromedriver", chrome_options = options)
    url = "https://www.imdb.com/chart/top?ref_=nv_mv_250"
    driver.get(url)
    #myascii = driver.page_source.encode("ascii", "ignore").decode("ascii")
    #print myascii
    soup = BeautifulSoup(driver.page_source, "lxml")
    table = soup.find("table", class_ = "chart full-width")

    film_list = []
    for td in table.find_all("td", class_ = "titleColumn"):
        table_data = td.text.strip().replace('\n','').replace('      ', '').encode("ascii", "ignore").decode("ascii")
        #print table_data
        rank = table_data.split(".")[0]
        #print rank 
        title = table_data.split(".")[1].split("(")[0]
        #print title
        year = table_data.split("(")[1][:-1]
        #print year
        a = td.find("a")
        #print a["href"]
        #print "\n"
        new_film = Film()
        new_film.rank = rank
        new_film.title = title
        new_film.year = year
        new_film.link = a["href"]
        film_list.append(new_film)



    return film_list
    driver.quit

def download_film_list(film_list) :

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome("/home/rahul/Downloads/chromedriver_linux64/chromedriver", chrome_options = options)
        
    for film in film_list:

        url = "https://www.imbd.com" + film.link
        #url ="https://www.imdb.com/title/tt0111161/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e31d89dd-322d-4646-8962-327b42fe94b1&pf_rd_r=H3JQCX530PCWC0XB9WK5&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_1" 
        driver.get(url)
        #print driver.page_source.encode("ascii", "ignore").decode("ascii")
        soup = BeautifulSoup(driver.page_source, "lxml")
        div = soup.find("div", class_="poster")
        a = div.find("a")
        first_addr = a["href"]
        link = "https://www.imdb.com" + first_addr
        driver.get(link)
        soup = BeautifulSoup(driver.page_source, "lxml")
        all_div = soup.find_all("div", class_="pswp__zoom-wrap")
        all_img = all_div[1].find_all("img")
        img_link = all_img[1]["src"]
        print img_link

        f = open("{0}.jpg".format(film.title.encode("utf8").replace(";", "")), "wb")
        f.write(requests.get(img_link).content)
        f.close()
    driver.quit

download_film_list(get_film_list())