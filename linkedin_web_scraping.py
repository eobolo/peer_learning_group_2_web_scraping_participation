# -*- coding: utf-8 -*-
"""LinkedIn_Web_Scraping.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1THdeV_6D41pTI7738so3ddFJIxTYF74m
"""

# Import relevant packages
import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
import pandas as pd # type: ignore
import datetime
import random
import math
from datetime import datetime

# Dictionary to map time posted options to LinkedIn's URL parameter values

time_posted_dict = {
    'ALL': '',
    'MONTH': 'r2592000',
    'WEEK': 'r604800',
    'DAY': 'r86400' # r86400 refers to the amount of seconds passed, in this case 24*60*60 = 86400
}

# Dictionary to map remote work options to LinkedIn's URL parameter values
remote_dict = {
    'ALL': '',
    'ON-SITE': '1',
    'REMOTE': '2',
    'HYBRID': '3'
}

def generate_main_linkedin_url(position, location, distance=10, time_posted='ALL', remote='ALL'):

    # Base URL for LinkedIn job search
    base_url = 'https://www.linkedin.com/jobs/search/'

    # Replace spaces in the job position with URL encoding (%20)
    url_friendly_position = position.replace(" ", "%20")

    # Construct the query parameters
    # The keywords and location are required parameters.
    query_params = f'?keywords={url_friendly_position}&location={location}'

    # Add the distance parameter if it is provided (default is 10 miles)
    if distance:
        query_params += f'&distance={distance}'

    # Add the time posted filter based on the user’s selection
    # This is retrieved from the time_posted_dict dictionary.
    if time_posted:
        time_posted_value = time_posted_dict.get(time_posted, '')
        query_params += f'&f_TPR={time_posted_value}'

    # Add the remote work filter based on the user’s selection
    # This is retrieved from the remote_dict dictionary.
    if remote:
        remote_value = remote_dict.get(remote, '')
        query_params += f'&f_WT={remote_value}'

    # Combine the base URL with the constructed query parameters
    url_search = base_url + query_params

    # Return the complete LinkedIn job search URL
    return url_search

def get_random_user_agent():
    """
    Selects and returns a random user agent string from a predefined list.
    """
    # List of different user agent strings to simulate various browsers and devices
    headers = [
        {'User-Agent': 'Mozilla/5.0'},
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
    ]

    selected_header = random.choice(headers)
    return selected_header

def fetch_jobs_until_success(url):
    got_200 = False
    while not got_200:
        response = requests.get(url, headers=get_random_user_agent())
        got_200 = response.status_code == 200
    return response

# Define default search parameters
position = 'Python Developer'
location = 'Toronto'
time_posted = 'ALL'
remote = 'ALL'

# Define valid options for each parameter
valid_time_posted = list(time_posted_dict.keys())  # ['ALL', 'MONTH', 'WEEK', 'DAY']
valid_remote = list(remote_dict.keys())  # ['ALL', 'ON-SITE', 'REMOTE', 'HYBRID']

# Function to get user input and validate it
def get_user_input(parameter, valid_options):
    while True:
        user_input = input(f"Enter {parameter} (options: {', '.join(valid_options)}): ")
        if user_input in valid_options:
            return user_input
        else:
            print("Invalid input. Please choose from the available options.")

# Get user input for search parameters
position = input("Enter job position: ")
location = input("Enter location: ")
time_posted = get_user_input("time posted", valid_time_posted)
remote = get_user_input("remote work", valid_remote)

# Generate the LinkedIn search URL based on the provided parameters
main_url = generate_main_linkedin_url(
    position,
    location,
    time_posted=time_posted,
    remote=remote
)

# Fetch job postings from the generated URL and ensure a successful response
response = fetch_jobs_until_success(main_url)

response = fetch_jobs_until_success(main_url)
soup = BeautifulSoup(response.text, 'html.parser')
all_jobs = int(soup.find('span', {'class': 'results-context-header__job-count'}).text)
print(f'There are a total of {all_jobs} jobs that will be scraped based on the given conditions.')

def get_url_next_10_positions(position, location,start_position, distance=10, time_posted='ALL', remote='ALL'):

    # Base URL for LinkedIn job search
    base_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search'

    # Replace spaces in position with URL encoding
    url_friendly_position = position.replace(" ", "%20")

    # Construct the query parameters
    query_params = f'?keywords={url_friendly_position}&location={location}'

    if distance:
        query_params += f'&distance={distance}'
    if time_posted:
        time_posted_value = time_posted_dict.get(time_posted, '')
        query_params += f'&f_TPR={time_posted_value}'
    if remote:
        remote_value = remote_dict.get(remote, '')
        query_params += f'&f_WT={remote_value}'
    query_params += f'&position=1&pageNum=0&start={start_position}'

    # Combine base URL with query parameters
    url_search = base_url + query_params

    return url_search

# Initialize an empty list to store job information
jobs = []

# Calculate the total number of pages to scrape based on the total number of jobs
total_pages = math.ceil(all_jobs / 10)

# Loop through each page of job listings (10 jobs per page)
for i in range(0, all_jobs, 10):

    # Determine the current page number
    current_page = i / 10 + 1 # +1 since start=0 is the first one

    # Generate the URL for the next set of 10 job positions
    target_url = get_url_next_10_positions(position, location, i, time_posted=time_posted, remote=remote)

    # Fetch the job postings from the generated URL until a successful response is received
    response = fetch_jobs_until_success(target_url)

    print(f"Parsing data for page: {int(current_page)}/{total_pages}")

    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    alljobs = soup.find_all('li')

    # Iterate through each job posting
    for job in alljobs:
        # If information is missing, use 'N/A' instead
        try:
            # Extract job title and company name from the job posting

            info = job.find('div', class_="base-search-card__info")
            title = info.find('h3', class_="base-search-card__title").text.strip() if info else 'N/A'
            company = info.find('h4', class_="base-search-card__subtitle").text.strip() if info else 'N/A'

            # Extract job location and job URL from the job posting
            metadata = job.find('div', class_="base-search-card__metadata")
            location_element = metadata.find('span', class_="job-search-card__location") if metadata else None
            location_job = location_element.text.strip() if location_element else None
            datetime_str = job.find('time', class_="job-search-card__listdate")['datetime'] if metadata else 'N/A'
            datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d')

            joburl_element = job.find('a', class_="base-card__full-link")
            joburl = joburl_element['href'] if joburl_element else 'N/A'

            # extract location_job
            if location_job:
                location_parts = location_job.split(", ")
                city = location_parts[0] if len(location_parts) > 0 else 'N/A'
                province = location_parts[1] if len(location_parts) > 1 else 'N/A'
                country = location_parts[2] if len(location_parts) > 2 else 'N/A'
            else:
                city = 'N/A'
                province = 'N/A'
                country = 'N/A'

            # process number of applicants
            try:
              job_response = requests.get(joburl)
              job_data = job_response.text
              job_soup = BeautifulSoup(job_data, "html.parser")
              num_applicants_element = job_soup.find("span", {"class": "num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet"})
              num_applicants = num_applicants_element.text.strip().split(" ")[0] if num_applicants_element else 0
            except requests.exceptions.RequestException as e:
                num_applicants = 0
            except Exception as e:
                num_applicants = 0

            # Store the extracted job information in a dictionary
            job_info = {
                'Title': title,
                'Company': company,
                'Url': joburl,
                'Date': datetime_obj,
                'Applicants': num_applicants,
                'City': city,
                'Province': province,
                'Country': country
            }
            # Add the job information to the list of jobs
            jobs.append(job_info)

        except Exception as e:
            # Print an error message if there is an issue processing a job
            # print(f"Error processing job: {e}")
            continue

df_jobs = pd.DataFrame(jobs, columns=['Title', 'Company', 'Url', 'Date', 'Applicants', 'City', 'Province', 'Country'])

df_jobs.replace("N/A", pd.NA, inplace=True)

df_jobs.head(40)

# Export DataFrame to CSV
date = datetime.now().strftime('%Y-%m-%d')
position = position.replace(" ", "_")
# Start with the base file name
file_name = f'LinkedIn_Jobs_{position}_{location}'

if time_posted != 'ALL':
    file_name += f'_LAST_{time_posted}'

# Append remote if it's not 'ALL'
if remote != 'ALL':
    file_name += f'_{remote}'

# Append the date to the file name
file_name += f'_{date}.csv'

# Export DataFrame to CSV
df_jobs.to_csv(file_name, index=False)