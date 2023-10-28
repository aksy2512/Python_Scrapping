import cfscrape
from bs4 import BeautifulSoup
import cloudscraper 
import undetected_chromedriver as uc 
from bs4 import BeautifulSoup
import re
driver = uc.Chrome()
yearly_salary_pattern = re.compile(r"₹([\d,]+) - ₹([\d,]+) a year")
monthly_salary_pattern = re.compile(r"Up to ₹([\d,]+) a month")
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["job_data"]
collection = db["jobs"]
def extract_salary(salary_str):
    yearly_salary_match = yearly_salary_pattern.search(salary_str)
    monthly_salary_match = monthly_salary_pattern.search(salary_str)

    if yearly_salary_match:
        min_salary = int(yearly_salary_match.group(1).replace(",", ""))
        max_salary = int(yearly_salary_match.group(2).replace(",", ""))
        return (min_salary + max_salary) // 2
    elif monthly_salary_match:
        monthly_salary = int(monthly_salary_match.group(1).replace(",", ""))
        yearly_salary = monthly_salary * 12
        return yearly_salary
    return None
def scrape_indeed_jobs(pages):
    jobs = []
    i = 0
    for page in range(pages):
        url = f'https://in.indeed.com/jobs?q=python+developer&start={page * 10}'
        driver.get(url)

        for _ in range(6):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        with open('indeed_jobs_soup.txt', 'w', encoding='utf-8') as file:
            file.write(str(soup))
        with open('indeed_jobs_soup.txt', 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        job_listings = soup.find_all('div', class_='job_seen_beacon')
        print(job_listings)
        for listing in job_listings:
            job_title_element = listing.find('span', class_='jobTitle')
            if job_title_element:
                job_title = job_title_element.text.strip()
            else:
                job_title = "Python Developer"

            company_element = listing.find('span', class_='css-1x7z1ps')
            if company_element:
                company = company_element.text.strip()
            else:
                company = None

            location_element = listing.find('div', class_='css-t4u72d')
            if location_element:
                location = location_element.text.strip()
            else:
                location = None

            summary_element = listing.find('div', class_='job-snippet')
            if summary_element:
                if summary_element.ul:
                    summary = summary_element.ul.get_text().strip()
                else :
                    summary = None
            else:
                summary = None
            salary_element = listing.find('div', class_='css-1ihavw2')
            if salary_element:
                salary_str = salary_element.text.strip()
                salary_range = extract_salary(salary_str)
                if salary_range:
                    salary= salary_range
                else:
                    salary = None
            else:
               salary  = None
            i=i+1
            job_data = {
                "num":i,
                "title": job_title,
                "company": company,
                "location": location,
                "summary": summary,
                "salary": salary
            }
            
            collection.insert_one(job_data)
            print("Job Title:", job_title)
            print("Company:", company)
            print("Location:", location)
            print("Summary:", summary)
            print("Salary:",salary)
            print()
job_listings = scrape_indeed_jobs(66)


driver.quit()

