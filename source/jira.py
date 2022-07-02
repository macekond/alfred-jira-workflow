# coding=utf-8

from feedback import Feedback
import urllib.parse
import json
import sys
import os.path
import re


feeds = Feedback()

server_url = sys.argv[2]

# check if the url is valid
if re.search(r'^(http|https)://', server_url) is None:
    server_url = 'https://' + server_url

if re.match(r'^((https|http)://)\w*(.|-\w{1,})?.\w{2,3}/?', server_url) is None:
    feeds.add_item(title='Invalid URL - Please check your server URL in  workflow configuration',
                   subtitle=server_url, valid='NO')

else:

    query = urllib.parse.quote(sys.argv[1])

    if re.search(r'^[a-zA-Z]', sys.argv[1]):
        # If the query starts with a letter, it's already a JIRA issue key
        ticket_url = "%s%s" % (server_url, query)
        feeds.add_item(title=query, subtitle=ticket_url,
                       valid='YES', arg=ticket_url, icon='icon.png')

    else:
        # Generate options for ticket number
        projects = sys.argv[3].split()
        
        # Sort projects by name if set in workflow configuration
        if sys.argv[4] == '1':
            projects.sort()

        for project in projects:
            ticket_name = "%s-%s" % (project, query)
            ticket_url = "%s%s" % (server_url, ticket_name)
            feeds.add_item(title=ticket_name, subtitle=ticket_url,
                           valid='YES', arg=ticket_url, icon='icon.png')

print(feeds)
