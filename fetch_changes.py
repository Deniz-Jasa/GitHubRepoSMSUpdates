import sys
import requests
import hashlib
import text_script as alert
from bs4 import BeautifulSoup

# Multiple GitHub API endpoints for README files
github_api_urls = [
    'https://api.github.com/repos/SimplifyJobs/Summer2024-Internships/readme',
    'https://github.com/jenndryden/Canadian-Tech-Internships-Summer-2024/readme'
    # Add more URLs as needed
]

# Multiple GitHub README page URLs
readme_urls = [
    'https://github.com/SimplifyJobs/Summer2024-Internships#readme',
    'https://github.com/jenndryden/Canadian-Tech-Internships-Summer-2024#readme'
    # Add more URLs as needed
]

phone_number_1 = sys.argv[1] # Passed as GitHub secrets
phone_number_2 = sys.argv[2]
account_sid = sys.argv[3]
auth_token = sys.argv[4]

# Function to retrieve and hash the README content
def get_readme_content(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        content = response.json()['content']
        return hashlib.md5(content.encode()).hexdigest()
    return None

# Function to read and update the previous README hash
def read_previous_readme_hash(filename):
    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def write_previous_readme_hash(filename, hash_value):
    try:
        with open(filename, 'w') as file:
            file.write(hash_value)
    except Exception as e:
        print(f"Error writing previous readme hash: {str(e)}")

# Function to scrape the company names from the README, skipping ↳ symbols
def scrape_company_names(readme_url):
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

# Loop through each set of URLs
for i in range(len(github_api_urls)):
    github_api_url = github_api_urls[i]
    readme_url = readme_urls[i]
    hash_filename = f"previous_readme_hash_{i}.txt"

    previous_readme_hash = read_previous_readme_hash(hash_filename)
    current_readme_hash = get_readme_content(github_api_url)

    if current_readme_hash and current_readme_hash != previous_readme_hash:
        write_previous_readme_hash(hash_filename, current_readme_hash)

        print(f"Success {current_readme_hash} for {github_api_url}")
        company_names = scrape_company_names(readme_url)

        sms_content = f"New update from '{readme_url}'. Keywords:\n" + "\n".join(company_names[:5]) + f"\nApply here: {readme_url}"
        alert.send_sms_notification(phone_number_1, sms_content, account_sid, auth_token)
        alert.send_sms_notification(phone_number_2, sms_content, account_sid, auth_token)
    else:
        print(f"No Changes for {github_api_url}")
