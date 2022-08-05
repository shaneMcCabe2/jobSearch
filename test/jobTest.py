from selenium import webdriver # web scraping functions
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By # locate elements on web pages
from selenium.webdriver.support.ui import WebDriverWait

import time # time-related processes
import pandas as pd # data manipulation and cleaning
import re # RegEx for text pattern matching


def load_page():

    url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=United%20States&locationId=&geoId=103644278&f_TPR=r86400&f_PP=102571732&position=1&pageNum=0'
    s = Service('C:/Users/Someone/Downloads/chromedriver_win32/chromedriver.exe')
    wd = webdriver.Chrome(service = s)
    wd.maximize_window()
    # wd.get("https://www.google.com")
    wd.get(url)
    print('Page loaded Successfully!')
    return wd


def get_job_count(webdriver):

    job_count_string = webdriver.find_element(By.CLASS_NAME, 'results-context-header__new-jobs').text
    # RegEx to match and return digits in job_count_string (this replaces nondigits with '')
    print(job_count_string)
    job_count = int(re.sub('\D', '', job_count_string))
    print(job_count)
    return job_count


def main():
    webdriver = load_page()
    job_count = get_job_count(webdriver)


if __name__=='__main__':
    main()



#button = webdriver.find_element(By.XPATH, "//html/body/div[1]/div/main/section[2]/button[.='Download']")
#ActionChains(webdriver).move_to_element(button).click().perform()
#button = WebDriverWait(webdriver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "infinite-scroller__show-more-button.infinite-scroller__show-more-button--visible[.='Download']")))
#webdriver.execute_script("arguments[0].click();", button)
#WebDriverWait(webdriver, 30).until(EC.presence_of_element_located(By.CLASS_NAME, 'infinite-scroller__show-more-button.infinite-scroller__show-more-button--visible'));
# wait.until(EC.invisibility_of_element_located(By.CLASS_NAME, 'infinite-scroller__show-more-button.infinite-scroller__show-more-button--visible'));
# webdriver.find_element(By.CLASS_NAME, 'infinite-scroller__show-more-button.infinite-scroller__show-more-button--visible').click()
#webdriver.execute_script('arguments[0].click();', find_element(By.XPATH, '//html/body/div[1]/div/main/section[2]/button'))

# WebDriverWait(webdriver, timeout=5).until(find_element(By.XPATH, '//main/section[2]/button').click())
