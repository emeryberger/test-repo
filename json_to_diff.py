def process():
    import json
    import sys
    json_data = sys.argv[1]
    
    data = json.loads(json_data)

    # Extract file path
    file_path = data['files'][0]['path']

    # Extract changed lines
    changed_lines = [change['content'] for change in data['files'][0]['chunks'][0]['changes']
                     if change['type'] in ('AddedLine', 'DeletedLine')]

    # Print the changed lines
    for line in changed_lines:
        print(line)

if __name__ == "__main__":
    process()
