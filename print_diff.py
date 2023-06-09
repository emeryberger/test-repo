import os
import requests

def get_pull_request_diff(owner, repo, pull_request_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_request_number}/files"
    print(f"URL = {url}")
    headers = {"Accept": "application/vnd.github.v3.diff"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def print_pull_request_diff(diff):
    print("Pull Request Diff:")
    print("------------------")
    print(diff)

def main():
    owner = os.environ.get("GITHUB_REPOSITORY_OWNER")
    repo = os.environ.get("GITHUB_REPOSITORY")
    pull_request_number = os.environ.get("GITHUB_PULL_REQUEST_NUMBER")

    diff = get_pull_request_diff(owner, repo, pull_request_number)
    print_pull_request_diff(diff)

if __name__ == "__main__":
    main()
