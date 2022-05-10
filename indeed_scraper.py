# USING SELENIUM
import random

import pandas as pd
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from tqdm import tqdm

# Using Selenium, and X-paths result is each individual clickcard


def extract_location(result):
    try:
        location = result.find_element_by_xpath('.//span[contains(@class,"location")]').text
    except:
        location = "None"
    return location

def extract_salary(result):
    try:
        salary = result.find_element_by_xpath('.//span[@class="salaryText"]').text
    except:
        salary = "None"
    return salary

def extract_job_title(result):
    try:
        title  = result.find_element_by_xpath('.//h2[@class="title"]//a').text
    except:
        title = result.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="title")
    return title

def extract_company(result):
    try:
        company = result.find_element_by_xpath('.//span[@class="company"]').text
    except:
        try:
            company = result.find_element_by_xpath('//*[@id="p_9d31f359e164959f"]/div[1]/div[1]/span[1]/a')
        except:
            company = "None"
    return company

def extract_link(result):
    try:
        link = result.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="href")
    except:
        link = "None"
    return link

def extract_rating(result):
    try:
        rating = result.find_element_by_xpath('.//span[@class="ratingsContent"]').text
    except:
        rating = "None"
    return rating

# Loading the driver
driver = webdriver.Chrome(ChromeDriverManager().install())

search_location = input('Enter city: ')

search_job = input('Enter job search: ')
search_job = '+'.join(search_job.split(' '))

driver.get('https://indeed.co.uk')

sleep(2)

finder_location = driver.find_element_by_xpath('//*[@id="text-input-where"]')
finder_location.send_keys(search_location)
finder_job = driver.find_element_by_xpath('//*[@id="text-input-what"]')
finder_job.send_keys(search_job)

sleep(2)

# Click Find Jobs

initial_search_button = driver.find_element_by_xpath(
    '//*[@id="whatWhereFormId"]/div[3]/button')
initial_search_button.click()

sleep(2)

# # Click Advanced Search
#
# advanced_serch = driver.find_element_by_xpath('/html/body/table[1]/tbody/tr/td/table/tbody/tr/td/form/table/tbody/tr/td[4]/a')
# advanced_serch.click()
#
# sleep(2)
#
# # set display limit of 30 results per page
#
# display_limit = driver.find_element_by_xpath('//*[@id="limit"]//option[@value="30"]')
# display_limit.click()
#
# # sort jobs by date rather than relevance
#
# sort_option = driver.find_element_by_xpath('//*[@id="sort"]//option[@value="date"]')
# sort_option.click()
#
# sleep(2)
#
# # Click Find Jobs
#
# find_jobs = driver.find_element_by_xpath('//*[@id="fj"]')
# find_jobs.click()
#
# # Click pop up asking for Email address
#
# try:
#     driver.find_element_by_xpath('//*[@id="popover-x"]/button').click()
# except:
#     print('no need')
#
# # Set lists for to store data

titles = []
companies = []
locations = []
salaries = []
reviews = []
links = []

# Check number of jobs to iterate over

jobs_in_city = driver.find_element_by_xpath('//*[@id="searchCountPages"]').text

# Search parameter check
print('City : ', search_location)
print('Job  : ', search_job)
print('No cards to iterate over : ', jobs_in_city[10:-5])

# Check if we are ready to go

job_card = driver.find_elements_by_xpath('//div[contains(@class,"clickcard")]')

print("TEST RUN:")
for job in job_card:
    print('\nTitle    : ', extract_job_title(job))
    print('Salary   : ', extract_salary(job))
    print('Company  : ', extract_company(job))
    print('Location : ', extract_location(job))
    print('Rating   : ', extract_rating(job))
    print('Link     : ', extract_link(job))
    print('\n')
    print('=' * 40)
    print('\n')

# # Set lists for to store data

titles = []
companies = []
locations = []
salaries = []
reviews = []
links = []

# let the driver wait 3 seconds to locate the element before exiting out
driver.implicitly_wait(3)

for i in tqdm(range(1, 21)):
    print("Page: {}".format(str(i)))
    job_card = driver.find_elements_by_xpath('//div[contains(@class,"clickcard")]')

    for job in job_card:
        #         Extract and assign all of the data
        titles.append(extract_job_title(job))
        companies.append(extract_company(job))
        locations.append(extract_location(job))
        salaries.append(extract_salary(job))
        reviews.append(extract_rating(job))
        links.append(extract_link(job))

    driver.get(
        'https://www.indeed.co.uk/jobs?q={}&l={}&sort=date&limit=30&radius=25&start={}'.format(
            '+'.join(search_job.split(' ')),
            search_location, str((i) * 30)))

df_city=pd.DataFrame()
df_city['Title']=titles
df_city['Company']=companies
df_city['Location']=locations
df_city['Salary']=salaries
df_city['Review']=reviews
df_city['Link']=links

print(df_city.head())

descriptions = []
company_links = []
for link in df_city['Link']:

    sleep(random.randint(3, 8))

    try:
        driver.get(link)
        description = driver.find_element_by_xpath('//div[@id="jobDescriptionText"]').text
    except:
        description = "None"
    try:
        co_link = driver.find_element_by_xpath('//*[@id="viewJobSSRRoot"]/div[1]/div[3]/div[1]/div[2]/div/div/div[1]/div[1]/a')
    except:
        co_link = 'None'
    company_links.append(co_link)
    descriptions.append(description)
    sleep(random.randint(3, 8))
    # try:
    #     driver.get(co_link)




df_city.to_csv('job_search27042021.csv')