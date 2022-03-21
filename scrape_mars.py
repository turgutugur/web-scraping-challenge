# Dependencies and Setup
from bs4 import BeautifulSoup as soup
from splinter import Browser
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# scrape all function 
def scrape_all():
    # set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # get the info from the news page
    news_title, news_p = scrape_news(browser)

    # build a dictionary with the info from scrapes
    marsData = {
        "newsTitle": news_title,
        "newsP": news_p,
        "image": scrape_img(browser),
        "facts": scrape_facts(browser),
        "hemispheres": scrape_hemispheres(browser),
        "lastModified": dt.datetime.now()
    }

    # stop the webbrowser 
    browser.quit()

    # display the webdriver
    return marsData


# scrape the news page
def scrape_news(browser):
    # Mars NASA news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    # convert the browser to html
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')
    # the title
    news_title = slide_elem.find('div', class_='content_title').get_text()
    # the paragraph
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    # return the news title and the paragraph 
    return news_title, news_p

# scrape image page
def scrape_img(browser):
    
    # image url
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    
    # go to the full image url
    full_image_link = browser.find_by_tag('button')
    full_image_link[1].click()

    # parse the result html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # find the image url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    # create an absulate url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    # return the image url
    return img_url

# scrape thru the facts page
def scrape_facts(browser):

    # facts url
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    # parse the result html with soup
    html = browser.html
    facts_soup = soup(html, 'html.parser')

    # find the facts location
    facts_location = facts_soup.find('div', class_='diagram mt-4')
    # find the html code for the fact table
    facts_table = facts_location.find('table')

    # create an empty string
    facts = ""
    # add the text to empty string and return
    facts += str(facts_table)
    return facts

# scrape thru hemisperes page
def scrape_hemispheres(browser):
    # base url
    hemis_url = 'https://marshemispheres.com/'
    browser.visit(hemis_url)

    # create a list to hold the img and titles
    hemis_img_url = []

    # set up a loop for all pages
    for i in range(4):
        # hemisphere dictionary
        hemisphereInfo = {}
    
        # finding the element on each loop
        browser.find_by_css('a.product-item img')[i].click()
    
        # finding sample image  and extract href
        sample_element = browser.find_by_text("Sample").first
        hemisphereInfo["img_url"] = sample_element["href"]
    
        # getting Hemisphere title
        hemisphereInfo["title"] = browser.find_by_css("h2.title").text
    
        # append hemisphere object to list
        hemis_img_url.append(hemisphereInfo)

        # navigate back
        browser.back()

    # return the hemisphere url with titles
    return hemis_img_url

# set up as a flask app
if __name__ == "__main__":
    print(scrape_all())

    
