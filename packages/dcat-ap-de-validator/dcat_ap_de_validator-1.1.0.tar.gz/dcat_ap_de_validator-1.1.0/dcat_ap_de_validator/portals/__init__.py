import requests
import json
import re


class Portal:
    def __init__(self, url):
        self.url = url
        if not url.endswith('/'):
            self.url = f"{url}/"
        self._packages = []

    def packages(self):
        api_path = "api/3/action/package_list"
        full_url = self.url + api_path

        response = requests.get(full_url)

        if response.status_code == 200:
            data = json.loads(response.content)
            result = data["result"]
            return result
        return []

    def package_url(self, package_name):
        return f"{self.url}dataset/{package_name}"

    def get_title(self):
        response = requests.get(self.url)
        # Extract the HTML content from the response
        html_content = response.content.decode()
        # Find the position of the opening and closing title tags
        title_start = html_content.find("<title>") + len("<title>")
        title_end = html_content.find("</title>")
        # Extract the contents of the title tag
        title = html_content[title_start:title_end].strip()
        # Remove any non-alphanumeric
        # characters from the title
        return re.sub(r'\W+', '', title)


class CKAN(Portal):
    def package_metadata_url(self, package_name):
        return f"{self.url}dataset/{package_name}.rdf"


class DKAN(Portal):
    def package_metadata_url(self, package_name):
        return f"{self.url}dcatapde/dataset/{package_name}.xml"  # DKAN
