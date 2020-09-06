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


# ### NASA Mars News

# In[3]:


# Define Url for the browser to launch
nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(nasa_url)
time.sleep(2)

# HTML object
html = browser.html
# Parse HTML with BS
soup = bs(html, 'html.parser')

# Retrieve all elements that contain quotes information
content_title = soup.find_all('div', class_='content_title')
article_teaser = soup.find_all('div', class_='article_teaser_body')


# In[4]:


# Manually grabbing the text...
news_title = content_title[1].text
news_p = article_teaser[0].text


# In[5]:


print(f'{news_title}: {news_p}')


# ### JPL Mars Space Images - Featured Image

# In[6]:


# URL of page to be scraped
jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(jpl_url)
time.sleep(2)

# Chromebroser, click on 'Full image', then 'more info'
browser.click_link_by_partial_text('FULL IMAGE')
browser.click_link_by_partial_text('more info')
# HTML object
html = browser.html
# Parse HTML with BS
soup = bs(html, 'html.parser')

# Featured image changes each time chromebrowser retrieve the image
mars_img = soup.find_all('figure', class_='lede')
mars_img_result = mars_img[0].a['href']
featured_image_url = 'https://www.jpl.nasa.gov' + mars_img_result 
print(featured_image_url)


# ### Mars Facts

# In[7]:


# Automatically scrape any tabular data from a page w pandas
mars_url = 'https://space-facts.com/mars/'
tables = pd.read_html(mars_url)


# In[8]:


# Fishing out wanted table, and transpose it
df = tables[0]


# In[9]:


# Raneme the column
df = df.rename(columns={0: 'Description',
                       1: 'Mars'})


# In[10]:


# Set the index to the `abb` column
df.set_index('Description', inplace=True)
df


# In[11]:


# Generate HTML tables from DataFrames
html_mars_table = df.to_html()


# In[12]:


# Convert df to html
df.to_html('mars_table.html')


# # Mars Hemispheres

# In[13]:


# # Instantiate a splinter browser
# browser = Browser('chrome', **executable_path, headless=False)

# Define URL to scrape title & url
marshem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(marshem_url)
time.sleep(2)

# HTML object
html = browser.html
# Parse HTML with BS
soup = bs(html, 'html.parser')

# Retrieve img title
# collapse_results = soup.find('div', class_='collapsible results')
# hem_title_list = collapse_results.find_all('a')

# Retrieve img url & title
itemlink = soup.find_all(class_='itemLink product-item')


# In[14]:


# Create an empty list to store dictionaries of imag_url & title
hemisphere_image_urls = []

# Create empty list ti store urls for image search 
url_list = []

# Retrieve img title and url one by one
for item in itemlink[1::2]:
    # Create an empty dictionary to store img_url & title
    hemisphere_dict = {}
    # Get title and add to the dictionary
    hemisphere_dict['title'] = item.h3.text

    # Get image URL and append to the empty list
    img_url_path = 'https://astrogeology.usgs.gov' + item.get('href')
    url_list.append(img_url_path)
    
    # Run a nested loop to the URL list that just got appended from above loop
    for url in url_list:
        # Retrieve page with the requests module
        response = requests.get(url)
        # Create bs object; parse with 'html.parser'
        soup = bs(response.text, 'html.parser')
        # Identify the wanted href
        sample = soup.find('a', href = True, text = 'Sample')
        # Get url from href and add to the dictionary
        hemisphere_dict['img_url'] = sample['href']

    # Add the dictionary to the list 
    hemisphere_image_urls.append(hemisphere_dict)
    
hemisphere_image_urls


# In[15]:


# Shut the browser down when done!
browser.quit()

