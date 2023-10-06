import sys
import requests
import hashlib
import text_script as alert
from bs4 import BeautifulSoup

# GitHub API endpoint for README file
# github_api_url = 'https://api.github.com/repos/Deniz-Jasa/TestReadme/readme'
github_api_url = 'https://api.github.com/repos/SimplifyJobs/Summer2024-Internships/readme'

# URL of the GitHub README page
readme_url = 'https://github.com/SimplifyJobs/Summer2024-Internships#readme'

phone_number_1 = sys.argv[1] # Passed as github secrets
phone_number_2 = sys.argv[2]

account_sid = sys.argv[3]
auth_token = sys.argv[4]

# Function to retrieve and hash the README content
def get_readme_content():
    response = requests.get(github_api_url)

    if response.status_code == 200:
        content = response.json()['content']
        return hashlib.md5(content.encode()).hexdigest()
    return None

# Function to read and update the previous README hash
def read_previous_readme_hash():
    try:
        with open('previous_readme_hash.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def write_previous_readme_hash(hash_value):
    try:
        with open('previous_readme_hash.txt', 'w') as file:
            file.write(hash_value)
    except Exception as e:
        print(f"Error writing previous readme hash: {str(e)}")

# Function to scrape the company names from the README, skipping ↳ symbols
def scrape_company_names():
    response = requests.get(readme_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        
        company_names = []
        skip_next = False
        count = 0
        
        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            if skip_next:
                skip_next = False
                continue
            company_name = columns[0].text.strip()
            
            # Check if the company name is ↳ (indicating multiple positions)
            if company_name == '↳':
                skip_next = True
                continue
            
            company_names.append(company_name)
            count += 1
            
            if count == 5:
                break
        
        return company_names
    return []

# Compare current and previous README hashes
previous_readme_hash = read_previous_readme_hash()
current_readme_hash = get_readme_content()

if current_readme_hash and current_readme_hash != previous_readme_hash:
    write_previous_readme_hash(current_readme_hash)

    print("Success")
    # Scrape the company names, skipping ↳ symbols
    company_names = scrape_company_names()

    sms_content = "New update from 'Summer2024-Internships'. Keywords:\n" + "\n".join(company_names[:5]) + "\nApply here nerd: https://github.com/SimplifyJobs/Summer2024-Internships"
    alert.send_sms_notification(phone_number_1,sms_content, account_sid, auth_token)
    alert.send_sms_notification(phone_number_2,sms_content, account_sid, auth_token)

else:
    print("No Changes")
    alert.send_sms_notification(phone_number_1, "No Changes", account_sid, auth_token)