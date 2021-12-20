#!/usr/bin/env python
# coding: utf-8

# In[27]:

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests

# In[28]:

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# In[3]:

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# In[4]:

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# In[5]:

slide_elem.find('div', class_='content_title')

# In[6]:

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# In[7]:

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# ### Featured Images

# In[8]
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# In[9]:

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# In[10]:

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# In[11]:

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# In[12]:

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# In[13]:

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# In[14]:

df.to_html()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ## Hemispheres 

# In[49]:

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# In[50]:

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
html_soup = soup(html, 'html.parser')

tags = html_soup.find_all('div', class_='description')
base_url = 'https://astrogeology.usgs.gov/'

hemispheres = {}

for tag in tags:
    child_element = tag.find('a', class_='itemLink product-item')
    page_url = child_element['href']
    full_page_url = f'{base_url}{page_url}'
    browser.visit(full_page_url)
    html1 = browser.html
    soup1 = soup(html1, 'html.parser')
    img_rel_url = soup1.find('img', class_='wide-image').get('src')
    img_url = f'{base_url}{img_rel_url}'
    hemispheres['img_url'] = img_url
    title = soup1.find('h2', class_='title').get_text()
    hemispheres['title'] = title
    hemisphere_image_urls.append(hemispheres)

# In[51]:

# 4. Print the list that holds the dictionary of each image url and title.
print(hemisphere_image_urls)

# In[52]:

# 5. Quit the browser
browser.quit()





