import pandas as pd
import os
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
import time

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # ### NASA Mars News
    # Pass news url to soup html parser
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html

    soup_news = bs(html, 'html.parser')

    # Get the latest news title and paragraph text
    time.sleep(5)
    news_title = soup_news.find_all('div', class_='content_title')[1].text    
    news_p = soup_news.find_all('div', class_='article_teaser_body')[0].text
    

    # ### JPL Mars Space Images - Featured Image
    space_image_url = 'https://www.jpl.nasa.gov'
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)
    html = browser.html

    soup_images = bs(html, 'html.parser')

    # values = soup_images.find_all('div', class_='carousel_items')
    url_ext = soup_images.find(class_='carousel_item')['style'].replace('background-image: url(','').replace("pg');","pg')")
    url_ext = url_ext[1:-2]
    url_ext

    # Concatenate url strings to get the featured image url
    featured_image_url = space_image_url + url_ext
    
    # ### Mars Facts
    # url for Mars facts webpage
    mars_facts_url = 'https://space-facts.com/mars/'

    # Pass the mars facts url into a pandas dataframe
    tables = pd.read_html(mars_facts_url)
    tables = tables[0]
    tables.rename(columns={0:'Text Description', 1:'Value'}, inplace=True)
    
    html_facts_table = tables.to_html()

    # ### Mars Hemispheres
    # Create the hemisphere image dictionary from the following location:
    hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    source_hem_url = "https://astrogeology.usgs.gov"
    browser.visit(hem_url)


    html_hem = browser.html
    soup = bs(html_hem, 'html.parser')

    image_urls = []

    for image_item in soup.find_all('div', class_='item'):
        hem_title = image_item.h3.text
        item_image = image_item.a.img['src']
        image_urls.append({"title" : hem_title, "img_url" : source_hem_url + item_image})

    marsdata = {}
    marsdata["news_title"] = news_title
    marsdata["news_p"] = news_p
    marsdata["featured_image_url"] = featured_image_url
    marsdata["table"] = html_facts_table
    marsdata["image_urls"] = image_urls

    browser.quit()
    return marsdata


