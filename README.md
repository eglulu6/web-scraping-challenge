# Web Scraping Homework - Mission to Mars

In this assignment, you will build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. The following outlines what you need to do.

## Step 1 - Scraping

### NASA Mars News
#Open the page with splinter
    #1. URL of website
        <url ="https://mars.nasa.gov/news/" />
    #2. Get website response
        <browser.visit(url)/>
    #3. Store response as text
        <html = browser.html/>
    #4. Create soup object
        <soup = BeautifulSoup(html, 'html.parser')/>

#Isolate the first news article title with a variable
    <div class="content-title"/>
#Isolate the paragraph for that article with a variable
    <div class="article_teaser_body"/>

### JPL Mars Space Images - Featured Image
#Open the page with splinter
    #1. URL of website
        <url ="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars" />
    #2. Get website response
        <browser.visit(url)/>
    #3. Store response as text
        <html = browser.html/>
    #4. Create soup object
        <soup = BeautifulSoup(html, 'html.parser')/>

#Find first img on page
     <img src = browser.find_by_css('img[class="BaseImage  object-contain"]').first />
#Click on img to get biggest img
     <img src = browser.find_by_css('img[class="BaseImage  object-contain"]').first.click() />
#Get img src for variable
     <img src vaiable = BeautifulSoup(img, class_= "BaseImage  object-contain")['src'] />
#Quit the browser
     <browser .quit() />
     
### Mars Facts
#Open the page with splinter
    #1. URL of website
        <url ="https://space-facts.com/mars/" />
    #2. Get website response
        <browser.visit(url)/>
    #3. Store response as text
        <html = browser.html/>
    #4. Create soup object
        <soup = BeautifulSoup(html, 'html.parser')/>
        
#Find the facts table
    <table id=tablepress-p-mars-no-2>
#Get table data
    <headers = soup.find_all("td", class_="column-1").text/>
    <rows = soup.find_all("td", class_="column-2").text/>
#Put table data into pandas df
    <df = pd.DataFrame(rows, index = headers)/>
    <df = pd.DataFrame(list(zip(rows, headers)))/>
#Use Pandas to convert the data to a HTML table string
    <html_string = df.to_html>
#Quit the browser
     <browser .quit() />
        
### Mars Hemispheres
        
#Open the page with splinter
    #1. URL of website
         <url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars" />
    #2. Get website response
        <browser.visit(url)/>
    #3. Store response as text
        <html = browser.html/>
    #4. Create soup object
        <soup = BeautifulSoup(html, 'html.parser')/>
# initialize an empty list for pymongo dict
        <hemi_list = [] />
#For loop to go thru all imgs
        <for img in page: />
    #Initialize an empty dict
            <hemi_dict = {} />   
    #Locate the img link
            <img_target = 'li[class="matchCentreSquadLabelContainer"]'/>
    #Click the link
            <browser.find_by_tag (target).click() />
    #Locate the download button & click the button
            <browser.click_link_by_text('Original') />
    #Save img url and title to variable        
            <sample_link = soup.find("a", target="blank", text="sample") />
            <hemi_dict['img_url'] = sample_link['href']/>
            <hemi_dict['title'] = soup.find_all("h2", class_="title").text/>  
    #Append the dict to list
            <hemi_list.append(hemi_dict) />
    #Click the back button
            <browser.back()/>
    #Click the next img link

- - -

## Step 2 - MongoDB and Flask Application

Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

* Start by converting your Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.

* Next, create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.

  * Store the return value in Mongo as a Python dictionary.

* Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.

* Create a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.

![final_app_part1.png](Images/final_app_part1.png)
![final_app_part2.png](Images/final_app_part2.png)

- - -

## Step 3 - Submission

To submit your work to BootCampSpot, create a new GitHub repository and upload the following:

1. The Jupyter Notebook containing the scraping code used.

2. Screenshots of your final application.

3. Submit the link to your new repository to BootCampSpot.

4. Ensure your repository has regular commits (i.e. 20+ commits) and a thorough README.md file

## Hints

* Use Splinter to navigate the sites when needed and BeautifulSoup to help find and parse out the necessary data.

* Use Pymongo for CRUD applications for your database. For this homework, you can simply overwrite the existing document each time the `/scrape` url is visited and new data is obtained.

* Use Bootstrap to structure your HTML template.

### Copyright

Trilogy Education Services © 2020. All Rights Reserved.
