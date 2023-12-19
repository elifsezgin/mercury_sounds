import os
import json
import requests

# os.environ['REQUESTS_CA_BUNDLE'] = requests.certs.where()

def generate_json_from_github(owner, repo, output_file, valid_extensions, token):
    headers = {"Authorization": f"Bearer {token}"}

    data = {}
    traverse_repository(owner, repo, data, valid_extensions, headers)

    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def traverse_repository(owner, api_url, data, valid_extensions, headers):
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            print(item['name'])
            if item['type'] == 'file' and item['name'].lower().endswith(tuple(valid_extensions)):
                file_name = os.path.splitext(item['name'])[0]
                raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{item['path']}"
                data[file_name] = raw_url
            elif item['type'] == 'dir':
                # Recursively traverse nested directories
                api_url = item["url"]
                traverse_repository(owner, api_url, data, valid_extensions, headers, )
    else:
        print(f"Failed to retrieve repository contents. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    owner = "elifsezgin"
    repo = "mercury_sounds"
    output_file = "sounds.json"
    token = os.environ.get("ELIF_GITHUB_ACCESS_TOKEN")

    valid_extensions = ['.wav', '.mp3', '.ogg', 'm4a', 'flac']

    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    try:
        print("Generating JSON data...")
        generate_json_from_github(owner, api_url, output_file, valid_extensions, token)
        print("JSON data generated successfully")

        print("Writing to JSON file...")
        print(f"JSON file '{output_file}' has been successfully created.")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
