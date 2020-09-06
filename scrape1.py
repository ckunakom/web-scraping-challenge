#!/usr/bin/env python
# coding: utf-8

# # Scraping

# In[1]:


# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
import time


# In[2]:


# Define path
executable_path = {'executable_path': 'c:/bin/chromedriver.exe'}

# Instantiate a splinter browser
browser = Browser('chrome', **executable_path, headless=False)

def scrape():




    # Define Url for the browser to launch
    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(nasa_url)
    time.sleep(2)

    # HTML object
    nasa_html = browser.html
    # Parse HTML with BS
    nasa_soup = bs(nasa_html, 'html.parser')
    # Retrieve all elements that contain quotes information
    content_title = nasa_soup.find_all('div', class_='content_title')
    article_teaser = nasa_soup.find_all('div', class_='article_teaser_body')

    # Shut the browser down when done!
    browser.quit()


    # In[ ]:


    # Manually grabbing the text...(?)
    news_title = content_title[1].text
    news_p = article_teaser[0].text


    # ### JPL Mars Space Images - Featured Image

    # In[ ]:


    # Trying XPATH way..

    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(2)


    # In[ ]:


    # Design an XPATH selector to grab the image

    ### THESE DON'T WORK ###
    xpath = '//div[contains(@src, “spaceimages”)]'
    # xpath = '//div/div[contains(@class="image"]/img'
    # xpath = '//div[contains(@class="image"]/img'
    # xpath = '//div[contains(@src, “spaceimages”)]'


    # In[ ]:


    # Use splinter to click on the image to bring up the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    # img.click()


    # In[ ]:


    # Scrape the browser into soup and use soup to find the full resolution image of mars
    # Save the image url to a variable called `img_url`
    html = browser.html
    soup = bs(html, 'html.parser')
    img_url = soup.find("img", class_="fancybox-image")["src"]
    img_url


    # In[ ]:


    # Shut the browser down when done!
    browser.quit()


    # In[ ]:


    # Instantiate a splinter browser
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    time.sleep(2)

    # HTML object
    jpl_html = browser.html
    # Parse HTML with BS
    jpl_soup = bs(jpl_html, 'html.parser')

    img = jpl_soup.find_all('figure', class_='lede')


    # Shut the browser down when done!
    browser.quit()


    # In[ ]:


    # imgthumb = jpl_soup.find('img', class_="thumb")
    # imgthumb1 = jpl_soup.find('a', class_="fancybox")
    # imgthumb2 = jpl_soup.footer.a.get("data-fancybox-href")
    # imgthumb2
    img_result = img[0].a['href']
    img_result


    # In[ ]:


    full_img = 'https://www.jpl.nasa.gov' + img_result 
    full_img


    # In[ ]:





    # In[ ]:





    # In[ ]:





    # In[ ]:





    # In[ ]:





    # In[ ]:





    # In[ ]:





    # In[ ]:





    # ### Mars Facts

    # In[ ]:


    # Automatically scrape any tabular data from a page w pandas
    mars_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_url)


    # In[ ]:


    # Fishing out wanted table, and transpose it
    df = tables[0]


    # In[ ]:


    # Raneme the column
    df = df.rename(columns={0: 'Description',
                        1: 'Mars'})


    # In[ ]:


    # Set the index to the `abb` column
    df.set_index('Description', inplace=True)
    df


    # In[ ]:


    # Generate HTML tables from DataFrames
    html_table = df.to_html()


    # In[ ]:


    # Convert df to html
    df.to_html('mars_table.html')


    # # Mars Hemispheres

    # In[34]:


    # Instantiate a splinter browser
    browser = Browser('chrome', **executable_path, headless=False)


    # Define URL to scrape title & url
    marshem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(marshem_url)
    time.sleep(2)

    # HTML object
    marshem_html = browser.html
    # Parse HTML with BS
    marshem_soup = bs(marshem_html, 'html.parser')
    # Retrieve img path
    description_class = marshem_soup.find('div', class_='collapsible results')


    # In[35]:


    hem_title = description_class.find_all('a')
    hem_title


    # In[26]:


    # url_list = []

    # for i in range(4):
    #     vst = {'url':hem_title[i]}
    #     url_list.append(vst)

    # display(url_list)


    # In[27]:


    links = soup.find_all(class_='itemLink product-item')
    links


    # In[37]:


    another_list = []

    for link in links:
        img = 'https://astrogeology.usgs.gov/' + link.get('href')
        another_list.append(img)

    another_list


    # In[39]:


    title_list = []

    url_list = []

    for url in another_list:
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        image = soup.find('a', href = True, text = 'Sample')
        url_image = image['href']
        url_list.append(url_image)  
        
        title1 = soup.find(class_='title').text.strip().replace(' Enhanced', '')
        title_list.append(title1)
        
    print(title_list, url_list)
        


    # In[40]:


    hem_url_image = []

    for i in range(4):
        hem_dict = {'title': title_list[i],
                'url': url_list[i]}
        hem_url_image.append(hem_dict)

    hem_url_image


    # In[ ]:





    # In[ ]:


    # image_name = []
    # for name in hem_title:
    #     image_name.append(name.text)
        
    # image_name


    # In[4]:


    # hem_imgurl = description_class[0].find_all('a')
    # hem_imgurl


    # In[ ]:





    # In[ ]:


   


    ##### DRAFT HERE ######## Getting IMAGE_URL
    # URL of page to be scraped ----- This is too manaual, it ain't right...
    ## I can't figure out how to use splinter for it to click on the image T^T ##


    
            

    # Shut the browser down when done!
    browser.quit()


    # In[ ]:






    # ### Jupyter Notebook Ended.

    # In[ ]:

    scrape_dictionary = {'title': content_title,
    'article': article_teaser,
    'image_mars': full_img,
    'table': df.to_html(),
    'marsmoon_title': hem_url_image,}
    # Converting your Jupyter notebook into a Python script called scrape_mars.py with a function called scrape
    # ................... HOW?????

    return scrape_dictionary