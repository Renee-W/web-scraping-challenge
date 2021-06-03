# Dependencies
import pandas as pd
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    
    # results are returned as an iterable list
    results = soup.find_all('div', class_='content_title')
    news_title=results[0].find('a').text.replace("\n", "")
    
    # results are returned as an iterable list
    results2 = soup.find_all('div', class_='rollover_description_inner')
    #results[0].find('a').text.replace("\nNASA's", "NASA's").replace(" \n", "")
    news_p=results2[0].text.replace("\n","")
    
    to_store={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image": featured_image(browser),
        "mars_facts":mars_facts(),
        "hemisphere":hemisphere(browser)
        }
    
    browser.quit()
    
    return to_store

def featured_image(browser):
    # URL of page to be scraped
    url2 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    # Retrieve page with the requests module
    browser.visit(url2) 
    browser.find_by_tag("button")[1].click()
    html=browser.html
    soup2=bs(html,"html.parser")
    results2 = soup2.find('img', class_="headerimage fade-in").get("src")
    featuredimageurl="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"+results2
    return featuredimageurl

def mars_facts():
    url3="https://space-facts.com/mars/"
    mars_df=pd.read_html(url3)[0]
    mars_df.columns=["Description","Value"]
    mars_df.set_index("Description", inplace=True)
    return mars_df.to_html()

def hemisphere(browser):
    url4="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    hemisphere_store=[]
    for i in range(4):
        temp={}
        browser.find_by_css("a.product-item img")[i].click()
        temp["title"]=browser.find_by_css("h2.title").text
        temp["url"]=browser.links.find_by_text("Sample").first["href"]
        hemisphere_store.append(temp)
        browser.back()
    return hemisphere_store

if __name__ =="__main__":
    print(scrape_all())
    
    