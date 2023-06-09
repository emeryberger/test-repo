import os
import requests

def get_diff(owner, repo, commit_sha, base_ref=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/compare"
    print(f"url = {url}")
    params = {
        "base": base_ref or commit_sha,
        "head": commit_sha
    }
    headers = {"Accept": "application/vnd.github.v3.diff"}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.text

def print_diff(diff):
    print("Commit Diff:")
    print("------------")
    print(diff)

def main():
    owner = os.environ.get("GITHUB_REPOSITORY_OWNER")
    repo = os.environ.get("GITHUB_REPOSITORY")
    event_name = os.environ.get("GITHUB_EVENT_NAME")

    if event_name == "pull_request":
        pull_request_number = os.environ.get("GITHUB_PULL_REQUEST_NUMBER")
        diff = get_diff(owner, repo, f"refs/pull/{pull_request_number}/merge")
    else:
        commit_sha = os.environ.get("GITHUB_SHA")
        base_ref = os.environ.get("GITHUB_BASE_REF")
        diff = get_diff(owner, repo, commit_sha, base_ref)

    print_diff(diff)

if __name__ == "__main__":
    main()
