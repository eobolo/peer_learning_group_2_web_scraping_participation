# peer_learning_group_2_web_scraping_participation

# LinkedIn Job Scraper

This Python script scrapes job data from LinkedIn based on specified criteria such as job title, location, time posted, and remote work options. It then saves the extracted data into a CSV file.


## Features

* Scrapes job title, company, URL, date posted, number of applicants, city, province, and country.
* Allows filtering by time posted (past day, week, month, or all).
* Allows filtering by remote work options (on-site, remote, hybrid, or all).
* Saves the scraped data into a CSV file named with the search criteria and date.


## Requirements

* Python 3.6 or higher
* The following Python packages:
    * `requests`
    * `beautifulsoup4`
    * `pandas`
    * `datetime`
    * `random`
    * `math`
    * `pipreqs`

```bash
pip install -r requirements.txt
```