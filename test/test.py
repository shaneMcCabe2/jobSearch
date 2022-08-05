

## This script will scrape new DA jobs from LI and append them to SQLite DB

## Note: many new jobs are uploaded around 12pm EST it appears (old jobs disappeared)


from selenium import webdriver # web scraping functions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By # locate elements on webpages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import time # time-related processes
import pandas as pd # data manipulation and cleaning
import re # RegEx for text pattern matching


# loads the page and returns the webdriver
def load_page():
    # linkedin job search page


    ####### url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=United%20States&locationId=&geoId=103644278&f_TPR=r86400&position=1&pageNum=0'
    url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=United%20States&geoId=103644278&f_TPR=r86400&f_JT=F&f_WT=2&f_E=2%2C3%2C4&position=24&pageNum=1&currentJobId=3200188222'


    ## installed geckodriver - a proxy for using W3C WebDriver clients with Gecko-based browsers
    ## https://github.com/mozilla/geckodriver - added to user path

    # define driver capabilities using FirefoxOptions
    # source: https://www.selenium.dev/documentation/webdriver/capabilities/firefox/
    options = Options()
    # options.headless = True
    options.add_argument('diable-infobars')
    options.add_argument('--disable-extensions')

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
    i = 1
    ## added 10 extra loops, sometimes a click or scroll down page would be skipped
    ## this ensures all jobs are loaded (unless there are 10+ skips)
    while i<= 0: # i <= int(job_count / 25) + 10:
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


def jobs_to_dataframe(jobs, webdriver):

    # initialize columns as arrays
    # data from cards
    job_id=[]
    job_title=[]
    company_name=[]
    location=[]
    date=[]
    job_link=[]

    # data from card details
    job_description = []
    seniority = []
    emp_type = []
    job_function = []
    industries = []
    applicants = []

    # get the data from each card
    for job in jobs:
        #job_id0 = job.find_element(By.CSS_SELECTOR, 'data-id')
        #job_id.append(job_id0)

        job_title0 = job.find_element(By.CSS_SELECTOR, 'div>h3.base-search-card__title').get_attribute('innerText')
        job_title.append(job_title0)

        company_name0 = job.find_element(By.CSS_SELECTOR,'div>h4.base-search-card__subtitle').get_attribute('innerText')
        company_name.append(company_name0)

        location0 = job.find_element(By.CSS_SELECTOR, 'div>div>span.job-search-card__location').get_attribute('innerText')
        location.append(location0)

        #date0 = job.find_element(By.CSS_SELECTOR, 'time.job-search-card__listdate--new').get_attribute('datetime')
        date0 = job.find_element(By.XPATH, '//div/div[2]/div/time').get_attribute('datetime')
        date.append(date0)

        # /html/body/div[1]/div/main/section[2]/ul/li[5]/div/a
        job_link0 = job.find_element(By.XPATH,'//div/a').get_attribute('href')
        job_link.append(job_link0)

    # click into each card to get more detailed data
    for item in range(len(jobs)):

        # click into each card
        try:
            job_click_path = f"//div[@class='base-serp-page']//li[{item+1}]//a[@class='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]']"
            job_click = webdriver.find_element(By.XPATH, job_click_path).click()
            time.sleep(.1)
        except:
            job_click_path = f"//div[@class='base-serp-page']//li[{item+1}]//a[@class='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]']"
            job_click = webdriver.find_element(By.XPATH, job_click_path).click()
            time.sleep(.1)
            # job_click_path = f"//div[@class='base-serp-page']//li[{item+1}]//a[@class='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]']"
            # job_element_wait = WebDriverWait(job, 5).until(expected_conditions.visibility_of_element_located((By.XPATH, job_click_path))).click()
            # time.sleep(.1)

        button = webdriver.find_element(By.XPATH, "//button[@class = 'show-more-less-html__button show-more-less-html__button--more']")
        # actions = ActionChains(webdriver)
        # actions.move_to_element(button)
        try:
            WebDriverWait(webdriver, 5).until(expected_conditions.element_to_be_clickable(button)).click()
        # actions.perform()
        # time.sleep(.1)
        except:
            while expected_conditions.visibility_of_element_located((By.XPATH, button)) == False:
                job_click_path = f"//div[@class='base-serp-page']//li[{item}]//a[@class='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]']"
                job_click = webdriver.find_element(By.XPATH, job_click_path).click()
                time.sleep(.1)
                job_click_path = f"//div[@class='base-serp-page']//li[{item+1}]//a[@class='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]']"
                job_click = webdriver.find_element(By.XPATH, job_click_path).click()
                time.sleep(.1)
        finally:
            button.click()
        #
        # show_more_click = job.find_element(By.XPATH, show_more_click_path).click()
        # time.sleep(.1)
        # except:
        #
        #         job_click_path = f"//div[@class='base-serp-page']//li[{item}]//a[@class='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]']"
        #         job_click = job.find_element(By.XPATH, job_click_path).click()
        #         time.sleep(.1)
        #         job_click_path = f"//div[@class='base-serp-page']//li[{item+1}]//a[@class='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]']"
        #         job_click = job.find_element(By.XPATH, job_click_path).click()
        #         time.sleep(.1)
        #
        #
        #
        #     show_more_click_path = "//button[@class = 'show-more-less-html__button show-more-less-html__button--more']"
        #     show_more_click = job.find_element(By.XPATH, show_more_click_path).click()
        #     time.sleep(.1)

        # added try and except blocks to account for job postings with incomplete data (ie: shows employment type but not seniority or industry)
        job_description_path = "//div[@class='show-more-less-html__markup']"
        job_description0 = job.find_element(By.XPATH, job_description_path).get_attribute('innerText')
        job_description.append(job_description0)


        # try:
        #     seniority_path = "//li[1]/span[@class='description__job-criteria-text description__job-criteria-text--criteria']"
        #     seniority0 = job.find_element(By.XPATH, seniority_path).get_attribute('innerText')
        #     seniority.append(seniority0)
        # except:
        #     seniority0 = 'Null'
        #     seniority.append(seniority0)
        #
        # try:
        #     emp_type_path = "//li[2]/span[@class='description__job-criteria-text description__job-criteria-text--criteria']"
        #     emp_type0 = job.find_element(By.XPATH, emp_type_path).get_attribute('innerText')
        #     emp_type.append(emp_type0)
        # except:
        #     emp_type0 = 'Null'
        #     emp_type.append(emp_type0)
        #
        # try:
        #     job_function_path = "//li[3]/span[@class='description__job-criteria-text description__job-criteria-text--criteria']"
        #     job_function_elements = job.find_elements(By.XPATH, job_function_path)
        #     for element in job_function_elements:
        #         job_function0 = []
        #         job_function1 = []
        #         job_function0.append(element.get_attribute('innerText'))
        #         job_function1 = ', '.join(job_function0)
        #     job_function.append(job_function1)
        # except:
        #     job_function1 = 'Null'
        #     job_function.append(job_function1)
        #
        # try:
        #     industries_path = "//li[4]/span[@class='description__job-criteria-text description__job-criteria-text--criteria']"
        #     industries_elements = job.find_elements(By.XPATH, industries_path)
        #     industries0 = []
        #     industries1 = []
        #     for element in industries_elements:
        #         industries0.append(element.get_attribute('innerText'))
        #         industries1 = ', '.join(industries0)
        #     industries.append(industries1)
        # except:
        #     industries1 = 'Null'
        #     industries.append(industries1)

        # #/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/figure/figcaption  //div[@class='base-serp-page']//section[@class='two-pane-serp-page__detail-view']
        # try:
        #     applicants_path = "//figcaption[@class='num-applicants__caption']"
        #     applicants0 = job.find_element(By.XPATH, applicants_path).get_attribute('innerText')
        # except:
        #     applicants0 = None
        #     print('Applicant data error')
        # applicants.append(applicants0)


    # create DataFrame and load data
    job_data = pd.DataFrame({
    'Title': job_title,
    'Company': company_name,
    'Location': location,
    'Date': date,
    'Link': job_link,
    'Description': job_description
    # 'Seniority': seniority,
    # 'Employment_Type': emp_type,
    # 'Function': job_function,
    # 'Industry': industries
    # 'Applicants': applicants
    })


    pd.set_option('display.max_columns', None)
    print(job_data.head())
    #print(job_data['Link'].to_string(index=False))

def main():
    webdriver = load_page()
    job_count = get_job_count(webdriver)
    jobs = scroll_jobs(job_count, webdriver)
    jobs_to_dataframe(jobs, webdriver)


if __name__=='__main__':
    main()
