## Tutorial for first part: https://maoviola.medium.com/a-complete-guide-to-web-scraping-linkedin-job-postings-ad290fcaa97f

## This script will scrape new DA jobs from LI and append them to SQLite DB

## Note: many new jobs are uploaded around 12pm EST it appears (old jobs disappeared)


from selenium import webdriver # web scraping functions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By # locate elements on web pages
# import time # time-related functions
import pandas as pd # data manipulation and cleaning
import re # RegEx for text pattern matching


# loads the page and returns the webdriver
def load_page():
    # linkedin job search page
    url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=United%20States&locationId=&geoId=103644278&f_TPR=r86400&position=1&pageNum=0'

    ## installed geckodriver - a proxy for using W3C WebDriver clients with Gecko-based browsers
    ## https://github.com/mozilla/geckodriver - added to user path

    # define driver capabilities using FirefoxOptions
    # source: https://www.selenium.dev/documentation/webdriver/capabilities/firefox/
    options = Options()
    options.headless = True
    wd = webdriver.Firefox(options=options)

    # load url
    wd.get(url)
    print('Page loaded Successfully!')
    return wd


# find the count location from page, find text, convert to int, and return count
def get_job_count(webdriver):

    job_count_string = webdriver.find_element(By.CLASS_NAME, 'results-context-header__new-jobs').text
    # RegEx to match and return digits in job_count_string (this replaces nondigits with '')
    job_count = int(re.sub('\D', '', job_count_string))
    print(job_count)
    return job_count


def main():
    webdriver = load_page()
    get_job_count(webdriver)


if __name__=='__main__':
    main()
