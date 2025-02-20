<h1><i>endHunter.py</i></h1>
<h2>This tool can be used to find <i>POSSIBLE</i> endpoints on javascript files.</h3>
<h3>⚠️ This tool uses regex to find the endpoints so it can generate false positives.⚠️</h3>
<br>
<h1>Usage</h1>

<b>The tool will visit each link found on a page and look for JS files and then look for possible endpoints in the JS file<b>

+ -t <i><b>Set the target website</i>
+ -o <i><b>Set the name of output file</i> 
+ -x <i><b>Set the headers to be used</i> (already has generic headers set)
+ -v <i><b>Verbose mode (will save Js files and URLs to the text file even if no endpoint was found)</i>
+ -d <i><b>Set a delay to use between requests (Default set to 0.3ms) </i>
+ -p <i><b>Match URL directory up to a specified depth. Default 3 </i>
<br>
<b><i>Example</i>: Python endHunter.py -t https://targetwebsite.com -o target.txt -d 0.7 -x {User-Agent: BugHunter} -v </br><br>
⚠️Remember to always use the http/https in target⚠️
</b>
<br>
<br>
<h1>💻Modules used💻</h1>

+ urllib3
+ requests 
+ argparse 
+ re 
+ time.sleep
## Installation
```
$ git clone https://github.com/oleomiranda/endhunter.git
```

```
pip install -r requirements.txt
```
