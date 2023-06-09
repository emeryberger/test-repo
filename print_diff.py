import pandas as pd
import glob
import os
import sys

def print_csv_diffs():
    head_commit = os.getenv('GITHUB_SHA')
    base_commit = os.getenv('GITHUB_BASE_REF')

    csv_files = glob.glob("*.csv")
    
    for file in csv_files:
        print(f'Diffs for {file}:')
        print('-' * 80)
        base_file_command = f'git show {base_commit}:{file}'
        head_file_command = f'git show {head_commit}:{file}'
        base_df = pd.read_csv(os.popen(base_file_command), header=None)
        head_df = pd.read_csv(os.popen(head_file_command), header=None)
        diff_df = head_df.compare(base_df)
        print(diff_df)
        print()
        
    files_changed_command = f"git diff --name-only main HEAD"
    # files_changed_command = f"git diff --name-only {base_commit} {head_commit}"
    files_changed = os.popen(files_changed_command).read().splitlines()

    csv_files = [file for file in files_changed if file.endswith('.csv')]

    print(f"files changed = {files_changed}")
    print(f"csv_files = {csv_files}")

    if not csv_files:
        print('No CSV files changed.')
        return

    for file in csv_files:
        print(f'Diffs for {file}:')
        print('-' * 80)
        base_file_command = f'git show {base_commit}:{file}'
        head_file_command = f'git show {head_commit}:{file}'
        base_df = pd.read_csv(os.popen(base_file_command), header=None)
        head_df = pd.read_csv(os.popen(head_file_command), header=None)
        diff_df = head_df.compare(base_df)
        print(diff_df)
        print()

if __name__ == '__main__':
    print_csv_diffs()
