import re
import csv
import json
import requests
import sys

import urllib.parse

# https://dblp.org/search/publ/api?q=author%3AEmery_D._Bergem%3A&format=json

def translate_name_to_dblp(name):
    # Ex: "Emery D. Berger" -> "http://dblp.uni-trier.de/pers/hd/b/Berger:Emery_D="
    # First, replace spaces and non-ASCII characters (not complete).
    name = re.sub(r' Jr\.', '_Jr.', name)
    name = re.sub(r' II', '_II', name)
    name = re.sub(r' III', '_III', name)
    name = re.sub(r'\'|\-|\.', '=', name)
    # Now replace diacritics.
    name = urllib.parse.quote(name, safe='=')
    name = re.sub(r'&', '=', name)
    name = re.sub(r';', '=', name)
    split_name = name.split(" ")
    last_name = split_name[-1]
    disambiguation = ""
    try:
        if int(last_name) > 0:
            # this was a disambiguation entry; go back.
            disambiguation = last_name
            split_name.pop()
            last_name = split_name[-1] + "_" + disambiguation
    except:
        pass
    split_name.pop()
    new_name = " ".join(split_name)
    new_name = new_name.replace(' ', '_')
    new_name = new_name.replace('-', '=')
    new_name = urllib.parse.quote(new_name)
    str_ = "https://dblp.org/pers/hd"
    last_initial = last_name[0].lower()
    str_ += f'/{last_initial}/{last_name}:{new_name}'
    return str_

def is_valid_account(account):
    # Check if the account is non-anonymous
    return not account.startswith('anonymous')

def has_reasonable_title(title):
    # Check if the title is reasonable
    return not title.startswith('Update csrankings-')

def has_valid_csv_files(files):
    # Check if only allowed CSV files are modified
    allowed_files = ['csrankings-[a-z].csv', 'country-info.csv', 'old/industry.csv', 'old/other.csv', 'old/emeritus.csv', 'old/rip.csv']
    for file in files:
        if re.match('.*\.csv', file):
            if not any(re.match(pattern, file) for pattern in allowed_files):
                return False
    return True

def has_no_spaces_after_commas(file):
    # Check if there are no spaces after commas in the file
    try:
        with open(file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                for value in row:
                    if re.search(r',\s', value):
                        return False
        return True
    except:
        return False

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
    if id == "NOSCHOLARPAGE":
        return True

    # Define the regular expression pattern for valid IDs
    pattern = r'^[a-zA-Z0-9_-]{7}AAAAJ$'
    
    # Check if the ID matches the pattern
    if not re.match(pattern, id):
        return False

    return True


def matching_name_with_dblp(name):
    # Check if the name matches the DBLP entry
    # Use requests library to fetch the DBLP page and check if the name is present
    # Try to fetch the author name and return the number of completions
    # (1 == an exact match).
    author_name = translate_name_to_dblp(name)
    dblp_url = f"https://dblp.org/search/publ/api?q=author%3A{name}%3A&format=json"
    try:
        response = requests.get(dblp_url)
        j = json.loads(response.text)
        completions = j['result']['completions']['@total']
        return int(completions)
    except requests.exceptions.RequestException:
        return 0

def is_eligible_faculty(homepage):
    # Check if the faculty member meets the inclusion criteria
    # You may want to implement additional checks here
    return True

def check_commit_validity(commit):
    valid = True
    files_modified = commit['modified_files']
    title = commit['title']
    account = commit['author']['account']
    homepage = commit['homepage']
    google_scholar_id = commit['google_scholar_id']
    name = commit['name']

    if not is_valid_account(account):
        print("Invalid account. Please use a non-anonymous account.")
        valid = False

    if not has_reasonable_title(title):
        print(f"Invalid commit title (\"{title}\"). Please provide a more descriptive title.")
        valid = False

    if not has_valid_csv_files(files_modified):
        print("Invalid file modification. Please only modify allowed CSV files.")
        valid = False

    for file in files_modified:
        if not has_no_spaces_after_commas(file):
            print(f"Invalid file ({file}). Please ensure there are no spaces after commas.")
            valid = False

    if not has_valid_homepage(homepage):
        print(f"Invalid homepage URL ({homepage}). Please provide a correct URL.")
        valid = False

    if not has_valid_google_scholar_id(google_scholar_id):
        print(f"Invalid Google Scholar ID ({google_scholar_id}). Please provide a valid identifier.")
        valid = False

    completions = matching_name_with_dblp(name)
    if completions == 0:
        print(f"Invalid name ({name}). Please ensure it matches the DBLP entry.")
        valid = False
    if completions > 1:
        print(f"Invalid name ({name}). This may be a disambiguation entry.")
        valid = False

    if not is_eligible_faculty(homepage):
        print("Invalid faculty inclusion. Please ensure the faculty meets the criteria.")
        valid = False

    return valid

def check_commit(modified_files):
    # Usage example
    bad_commit = {
        'author': {
            'account': 'john_doe'
        },
        'title': 'Update csrankings-a.csv',
        'modified_files': ['csrankings-a.csv'],
        'homepage': 'https://www.emerybergen.com',
        'google_scholar_id': 'dbfeR3YAAAAJ',
        'name': 'Wei Zhang'
    }

    good_commit = {
        'author': {
            'account': 'john_doe'
        },
        'title': 'Add Emery to csrankings-a.csv', # this is still not great, wrong file
        'modified_files': modified_files, # ['csrankings-a.csv'],
        'homepage': 'https://www.emeryberger.com',
        'google_scholar_id': 'dbfeR3YAAAAJ',
        'name': 'Emery D. Berger'
    }

    commit = good_commit

    is_commit_valid = check_commit_validity(commit)
    if is_commit_valid:
        print("All sanity checks passed.")
        sys.exit(0)
    else:
        print(f"Commit validity: {is_commit_valid}")
        sys.exit(-1)

if __name__ == "__main__":
    print(f"args = {sys.argv}")
    for fname in sys.argv[1:]:
        diff_fname = f"{fname}.diff"
        with open(diff_fname, 'r') as f:
            print(f.read())
            
    check_commit(sys.argv[1:])
    
