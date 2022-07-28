## Tutorial for first part: https://maoviola.medium.com/a-complete-guide-to-web-scraping-linkedin-job-postings-ad290fcaa97f

## This script will scrape new DA jobs from LI and append them to SQLite DB

## Note: many new jobs are uploaded around 12pm EST it appears (old jobs disappeared)


from selenium import webdriver # web scraping functions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By # locate elements on webpages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

import time # time-related processes
import pandas as pd # data manipulation and cleaning
import re # RegEx for text pattern matching


# loads the page and returns the webdriver
def load_page():
    # linkedin job search page


    ####### url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=United%20States&locationId=&geoId=103644278&f_TPR=r86400&position=1&pageNum=0'
    url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=United%20States&locationId=&geoId=103644278&f_TPR=r86400&f_PP=102571732&position=1&pageNum=0'


    ## installed geckodriver - a proxy for using W3C WebDriver clients with Gecko-based browsers
    ## https://github.com/mozilla/geckodriver - added to user path

    # define driver capabilities using FirefoxOptions
    # source: https://www.selenium.dev/documentation/webdriver/capabilities/firefox/
    options = Options()
    # options.headless = True
    wd = webdriver.Firefox(options=options)
    wd.maximize_window()
    # load url
    wd.get(url)
    # script crashes if webpage doesn't load on time, sleep to ensure it loads
    time.sleep(3)
    print('Page loaded Successfully!')
    return wd


# find the count location from page, find text, convert to int, and return count
def get_job_count(webdriver):

    job_count_string = webdriver.find_element(By.CLASS_NAME, 'results-context-header__new-jobs').text
    # RegEx to match and return digits in job_count_string (this replaces nondigits with '')
    job_count = int(re.sub('\D', '', job_count_string))
    print(job_count)
    return job_count



## https://www.selenium.dev/documentation/webdriver/waits/   ?????
# Linkedin loads more jobs as you scroll the page, this function scrolls for us
def scroll_jobs(job_count, webdriver):
    i = 0
    ## added 10 extra loops, sometimes a click or scroll down page would be skipped
    ## this ensures all jobs are loaded (unless there are 10+ skips)
    while i <= 5: # int(job_count / 25) + 10:
        webdriver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        i = i + 1
        try:
            webdriver.find_element(By.CLASS_NAME, 'infinite-scroller__show-more-button.infinite-scroller__show-more-button--visible').click()
            time.sleep(.1)
        except:
            pass
            time.sleep(.1)

    job_list = webdriver.find_element(By.CLASS_NAME, 'jobs-search__results-list')
    jobs = job_list.find_elements(By.TAG_NAME, 'li') # return list
    print(len(jobs))
    return jobs


def jobs_to_dataframe(jobs):

    # initialize columns as arrays
    job_id=[]
    job_title=[]
    company_name=[]
    location=[]
    date=[]
    job_link=[]

    for job in jobs:
        #job_id0 = job.find_element(By.CSS_SELECTOR, 'data-id')
        #job_id.append(job_id0)

        job_title0 = job.find_element(By.CSS_SELECTOR, 'h3.base-search-card__title').get_attribute('innerText')
        job_title.append(job_title0)

        company_name0 = job.find_element(By.CSS_SELECTOR,'h4.base-search-card__subtitle').get_attribute('innerText')
        company_name.append(company_name0)

        location0 = job.find_element(By.CSS_SELECTOR, 'div>div>span.job-search-card__location').get_attribute('innerText')
        location.append(location0)

        date0 = job.find_element(By.CSS_SELECTOR, 'div>div>time.job-search-card__listdate--new').get_attribute('datetime')
        date.append(date0)

        job_link0 = job.find_element(By.CSS_SELECTOR,'h4>a.hidden-nested-link').get_attribute('href')
        job_link.append(job_link0)

    # create DataFrame and load data
    job_data = pd.DataFrame({#'ID': job_id,
    'Title': job_title,
    'Company': company_name,
    'Location': location,
    'Date': date,
    'Link': job_link
    })

    # pd.set_option('display.max_columns', None)
    # print(job_data.head())

def main():
    webdriver = load_page()
    job_count = get_job_count(webdriver)
    jobs = scroll_jobs(job_count, webdriver)
    jobs_to_dataframe(jobs)


if __name__=='__main__':
    main()
