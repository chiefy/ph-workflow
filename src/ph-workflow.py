#!/usr/bin/python
# encoding: utf-8

import sys
import urllib2
import json

from workflow import Workflow

def main(wf):
    args = wf.args
    
    if wf.update_available:
        wf.add_item("An update is available!", autocomplete='workflow:update', valid=False)

    api_root = "https://api.producthunt.com/v1"
    api_token = "33f02c7e9abaeafb5eb221a9f8d59b83019160dd8231f53e5709f11704f082b8"

    request = urllib2.Request("%s/posts" % api_root, None, { "Authorization" : "Bearer %s" % api_token })
    response = urllib2.urlopen(request)
    posts = json.loads(response.read())['posts']
    
    for post in posts:
        product_name = post['name']
        subtitle = "Votes: %s - %s" % (post['votes_count'], post['tagline'])
        url = post['redirect_url']
        wf.add_item(product_name, subtitle, arg=url, valid=True)

    # Send output to Alfred
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(update_settings={
        'github_slug': 'chiefy/ph-workflow',
        'version': 'v1.0.0',
    })
    sys.exit(wf.run(main))
