import urllib.parse as urlparser
import requests
import argparse
import re
from time import sleep

class endHunter():
  def __init__(self):
    self.links_to_visit = []
    self.visited_links = []
    self.js_visited = []
    self.get_arguments()


  def get_arguments(self):
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="The site you want to find the possibles endpoints", dest="target")
    parser.add_argument("-o", "--output", help="File to write the results", dest="file")
    parser.add_argument("-v", "--verbose", help="Will write the Url and JS url to the file even if no possible endpoint was found", action="store_true")
    parser.add_argument("-d", "--delay", help="Add delay between each request", dest="delay", default=0.3)
    parser.add_argument("-x", help="Define the header to be used on requests", dest="header", default={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'})

    arguments = parser.parse_args()

    self.target_site = arguments.target
    self.file = arguments.file
    self.verbose = arguments.verbose
    self.delay = arguments.delay
    self.target_no_http = self.target_site.replace("https://", "").replace("http://", "")
    
    self.headers = arguments.header
    self.visited_links.append(self.target_site)
    self.find_links(self.target_site)

  def find_links(self, url):
    req = requests.get(url, headers=self.headers)
    if req.status_code != 200:
      print(f"The request to {url} returned status code {req.status_code}")
      return 0
    content = req.text

    js_links = self.link_getter(content)
    self.save_js_links(url, js_links)

    for target_link in self.links_to_visit:
      self.links_to_visit.remove(target_link)
      ignored_link = self.should_ignore(target_link)
      if ignored_link:
        continue
      target_link = self.url_format_verifier(target_link)
      if self.target_no_http in target_link:
        self.visited_links.append(target_link)
        print(f"target link -> {target_link}")
        sleep(float(self.delay))                
        self.find_links(target_link)

  def link_getter(self, content):

    link_list = re.findall(r'(?:href=["\'\`]|src=["\'])((?:https?:\/\/|\/+|\.+).*?)(?:"|\'|\`)', content)
    js_links = re.findall(r'(?:href|src)="([^"]+\.js)', content)

    link_list = set(link_list)
    set_visited = set(self.visited_links)
    new_list = link_list - set_visited
    self.links_to_visit = self.links_to_visit + list(new_list)

    js_links = set(js_links)
    set_js_visited = set(self.js_visited)
    new_js_links = js_links - set_js_visited

    return new_js_links

  def save_js_links(self, current_url, js_links):
    current_url = self.url_format_verifier(current_url)

    for js_link in js_links:

        if re.match('^(?!.*http).*$', js_link):
            js_link = urlparser.urljoin(self.target_site, js_link)
        
        self.js_visited.append(js_link)
        print(f"JS LINK -> {js_link}")
        self.search_on_js(js_link, current_url)

  def search_on_js(self, url, foundAt):
    sleep(float(self.delay))
    site = requests.get(url)
    content = site.text

    endpoints = re.findall(r'(?:")(\/\w+[^\s|\[|\]|\(|\)|\+|\^|\.|,]+)(?:")', content)

    self.write_to_file(url, foundAt, endpoints)

  def should_ignore(self, url):

    if re.search(r'(\.css\/*|\.jpg\/*|\.png\/*|\.ico\/*|\.svg\/*|\.js\/*|\.json\/*|\.jpeg\/*|\.pdf\/*)', url):
        return True
    return False

  def url_format_verifier(self, url):
    if re.search(r'[^\/]$', url):
      url = url + "/"
    if re.search('^http.+', url):
      url = urlparser.urljoin(self.target_site, url)
    return url

  def write_to_file(self, url, foundAt, endpoints):
    fileToWrite = open(self.file, "a")
    endpointList = []
    for endpoint in endpoints:
        if endpoint not in endpointList:
            endpointList.append(endpoint)

    if len(endpointList) > 0 or self.verbose:
        text = f"""
Js link:{url}\n
Found at:{foundAt}\n
Possible endpoints: {endpointList}\n\n\n
"""

        fileToWrite.write(text)
        fileToWrite.close()

endHunter()