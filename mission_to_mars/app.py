# import dependancies
import pandas as pd
from flask import Flask, jsonify, render_template
from jinja2 import Environment, PackageLoader, select_autoescape
import requests
import time
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import time

# Setup Flask app
app = Flask(__name__)

##################################################################################################
# other fuctions to use in @app scrape function
##################################################################################################

def news():
    ################## NASA Mars News ######################

    # initialize dict for mars_dict_list in pymongo
    article_dict = {}

    # SETUP SPLINTER
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of website
    mars_news_url = "https://mars.nasa.gov/news/"

    # Get website response
    browser.visit(mars_news_url)

    # Pause for page load
    time.sleep(3)

    # Store response as text
    mars_news_html = browser.html

    # Create soup object
    news_soup = BeautifulSoup(mars_news_html, 'html.parser')

    #Isolate the first news article title <div class="content-title"/>
    all_content_titles = news_soup.find_all("div", class_="content_title")

    #capture result in variable
    latest_title = all_content_titles[1].text.strip()

    #Isolate the paragraph for that article <div class="article_teaser_body"/>
    all_article_teaser_body = news_soup.find_all('div', class_="article_teaser_body")

    #capture result in variable
    latest_paragraph = all_article_teaser_body[0].text.strip()

    #quit broswer session
    browser.quit()

    #add items to dict
    article_dict['latest_title'] = latest_title
    article_dict['latest_paragraph'] = latest_paragraph

    # render an index.html template for jinja in html file
    news = [article_dict]
    return render_template("index.html", news=news)

########################################################

def images():
    ####### JPL Mars Space Images - Featured Image #########

    # SETUP SPLINTER
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # OPEN PAGE WITH SPLINTER

    # 1. URL of website
    jpl_imgs_url ="https://www.jpl.nasa.gov/images?search=&category=Mars"

    # 2. Get website response
    browser.visit(jpl_imgs_url)

    # 3. Store response as text
    #jpl_imgs_html = browser.html

    # 4. Create soup object
    #jpl_soup = BeautifulSoup(jpl_imgs_html, 'html.parser')

    # NAVIGATE TO THE FIRST IMG's PAGE

    #Find & click first img on page <img src = browser.find_by_css('img[class="BaseImage  object-contain"]').first />
    browser.find_by_css('img[class="BaseImage  object-contain"]').first.click()

    # Store response as text
    featured_img_html = browser.html

    # Create soup object of new page
    featured_soup = BeautifulSoup(featured_img_html, 'html.parser')

    # capture fullsize featured img url
    featured_image_url = featured_soup.find('img', class_= 'BaseImage')['src']

    # quit browser session
    browser.quit()

    # render an index.html template for jinja in html file
    image = {'image':featured_image_url}
    return render_template("index.html", image=image)

########################################################

def facts_table():
    ################## Mars Facts webpage ##################

    # SETUP SPLINTER
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of website
    facts_url ="https://space-facts.com/mars/"

    # Store response as text
    facts_html = pd.read_html(facts_url)

    # get first table
    facts_table = facts_html[0]

    #give columns headers
    facts_table.columns = ['Title', 'Fact']

    # convert df into html
    facts_html_table = facts_table.to_html

    # quit browser session
    browser.quit()
    
    # render an index.html template for jinja in html file
    return render_template("index.html", facts_html_table=facts_html_table)

########################################################

def four_hemispheres():
    ###### USGS Astrogeology site - Mars Hemispheres #######

    # SETUP SPLINTER
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #1. URL of website
    hemi_url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    #2. Get website response
    browser.visit(hemi_url)

    #3. Store response as text
    all_hemi_html = browser.html

    #4. Create soup object
    all_hemi_soup = BeautifulSoup(all_hemi_html, 'html.parser')

    #find all imgs
    hemi_all_img = all_hemi_soup.find_all('img', class_='thumb')

    # Iitialize dict for py mongo
    hemi_dict = {}

    # Start loop to get img and title on all hemishpere
    for img in hemi_all_img:

        #Locate img link
        img_target = 'img[class="thumb"]'

        #Click the link
        browser.find_by_tag(img_target).click()

        #Store response as text
        one_hemi_html = browser.html

        #Create soup object
        one_hemi_soup = BeautifulSoup(one_hemi_html, 'html.parser')

        #Save img url and title to variable        
        hemi_dict['img_url'] = one_hemi_soup.find("a", text="Original")['href']

        #Save hemishpere title
        hemi_dict['title'] = one_hemi_soup.find("h2", class_="title").text

        #Click the back button
        browser.back()

    # quit browser session
    browser.quit()

    # render an index.html template for jinja in html file
    return render_template("index.html", hemi_dict=hemi_dict)

#################################################################################################

# create home landing page
@app.route('/')
def scrape():
    return four_hemispheres(),facts_table(),facts_table(), images(),news()

#################################################################################################

if __name__ == '__main__':
    app.run(debug=True)