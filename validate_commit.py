import re
import csv
import requests
import sys

def is_valid_account(account):
    # Check if the account is non-anonymous
    return not account.startswith('anonymous')

def has_reasonable_title(title):
    # Check if the title is reasonable
    return not title.startswith('Update csrankings-')

def has_valid_csv_files(files):
    # Check if only allowed CSV files are modified
    allowed_files = ['csrankings-[a-z].csv', 'country-info.csv', 'old/industry.csv']
    for file in files:
        if not any(re.match(pattern, file) for pattern in allowed_files):
            return False
    return True

def has_no_spaces_after_commas(file):
    # Check if there are no spaces after commas in the file
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            for value in row:
                if re.search(r',\s', value):
                    return False
    return True

def has_valid_homepage(homepage):
    # Check if the homepage URL is correct
    # Use requests library to fetch the page and check the response
    try:
        response = requests.get(homepage)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def has_valid_google_scholar_id(id):
    # Check if the Google Scholar ID is valid
    # You may want to implement additional checks here
    return True

def has_matching_name_with_dblp(name):
    # Check if the name matches the DBLP entry
    # Use requests library to fetch the DBLP page and check if the name is present
    dblp_url = f"http://dblp.org/search?q={name}"
    try:
        response = requests.get(dblp_url)
        return name in response.text
    except requests.exceptions.RequestException:
        return False

def is_eligible_faculty(homepage):
    # Check if the faculty member meets the inclusion criteria
    # You may want to implement additional checks here
    return True

def check_commit_validity(commit):
    valid = True
    files_modified = commit.get_modified_files()
    title = commit.get_title()
    account = commit.get_author().get_account()
    homepage = commit.get_homepage()
    google_scholar_id = commit.get_google_scholar_id()
    name = commit.get_name()

    if not is_valid_account(account):
        print("Invalid account. Please use a non-anonymous account.")
        valid = False

    if not has_reasonable_title(title):
        print("Invalid title. Please provide a more descriptive title.")
        valid = False

    if not has_valid_csv_files(files_modified):
        print("Invalid file modification. Please only modify allowed CSV files.")
        valid = False

    for file in files_modified:
        if not has_no_spaces_after_commas(file):
            print(f"Invalid file {file}. Please ensure there are no spaces after commas.")
            valid = False

    if not has_valid_homepage(homepage):
        print("Invalid homepage URL. Please provide a correct URL.")
        valid = False

    if not has_valid_google_scholar_id(google_scholar_id):
        print("Invalid Google Scholar ID. Please provide a valid alphanumeric identifier.")
        valid = False

    if not has_matching_name_with_dblp(name):
        print("Invalid name. Please ensure it matches the DBLP entry.")
        valid = False

    if not is_eligible_faculty(homepage):
        print("Invalid faculty inclusion. Please ensure the faculty meets the criteria.")
        valid = False

    return valid

# Usage example
commit = {
    'author': {
        'account': 'john_doe'
    },
    'title': 'Update csrankings-abc.csv',
    'modified_files': ['csrankings-abc.csv'],
    'homepage': 'https://example.com',
    'google_scholar_id': 'abcdef123456',
    'name': 'John Doe'
}

is_commit_valid = check_commit_validity(commit)
print(f"Commit validity: {is_commit_valid}")
if is_commit_valid:
    sys.exit(0)
else:
    sys.exit(-1)
    
