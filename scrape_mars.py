def scrape():

    from splinter import Browser
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    import re

    ##Latest Article

    url = 'https://mars.nasa.gov/news'

    executable_path = {'executable_path':'chromedriver.exe'}

    browser = Browser('chrome', **executable_path, headless = False)

    browser.visit(url)

    soup = BeautifulSoup(browser.html, 'lxml')

    latest_article_text = soup.find('div', class_ = 'article_teaser_body').text
    latest_article_title = soup.find('div', class_ = 'content_title').a.text

    ##Featured image url

    executable_path = {'executable_path':'chromedriver.exe'}

    browser = Browser('chrome', **executable_path, headless = False)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    string = soup.find('article', class_ = 'carousel_item')['style']

    string_split = string.split('\'')

    featured_image_url = 'https://www.jpl.nasa.gov/' + string_split[1]

    ##Twitter Scrape

    url = 'https://twitter.com/marswxreport?lang=en'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')

    tweets = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    for tweet in tweets:
        if 'Sol' in tweet.text:
            mars_weather = tweet.text
            break

    ## Mars facts table

    url = 'https://space-facts.com/mars/'

    df = pd.read_html(url)

    weather_table = df[0].to_html()

    ##Mars Hemispheres images

    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser = Browser('chrome', **executable_path, headless = False)

    browser.visit(url4)

    html = browser.html

    big_soup = BeautifulSoup(html, 'html.parser')

    links = big_soup.find_all('h3')

    hemispheres = []

    for link in links :
        browser.click_link_by_partial_text(link.text)
        img_dict = {}
        lil_soup = BeautifulSoup(browser.html, 'html.parser')
        img_dict['img_url'] = lil_soup.find('a', text = re.compile('Original'))["href"]
        img_dict['title'] = link.text
        hemispheres.append(img_dict)
        browser.click_link_by_partial_text('Back')

    all_dict = {
        "Latest Article" : [latest_article_text, latest_article_title],
        'Featured Image' : featured_image_url,
        "Weather Tweet" : mars_weather,
        "Fact Table": weather_table,
        'Hemisphere Images' : hemispheres
    }

    print(all_dict)

    return all_dict