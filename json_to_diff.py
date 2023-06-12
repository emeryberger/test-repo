def process():
    import json # test
    import sys
    json_file = sys.argv[1]

    with open(json_file, "r") as f:
        json_data = f.read()

    data = json.loads(json_data)

    # Extract file paths

    changed_lines = {}
    
    for d in data['files']:
        file_path = d['path']
        print(file_path)
        changed_lines[file_path] = []

        for chunk in d['chunks']:
            for change in chunk['changes']:
                if change['type'] == 'AddedLine':
                    changed_lines[file_path].append(change)

    print(changed_lines)
    
if __name__ == "__main__":
    process()
