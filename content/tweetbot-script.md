Title: Tweetbot Script
Date: 2013-01-06 04:53:47
Tags: scripting, python, twitter
Slug: tweetbot-script
Author: Tim Bueno
Summary: Tiny script to automate Tweetbot

On my Macbook, I often run into links to specific posts on Twitter from sites such as Hacker News. However I'd prefer it if these links did not open in Safari, but Tweetbot instead. I wrote a quick script that does exactly that. Assign my script to a hotkey of your choosing using something like Keyboard Maestro and you are all set.

If you are viewing a person's Twitter profile and invoke the script it will open their profile in Tweetbot. Specific tweets will also open in Tweetbot.

Unfortunately, this python script relies on Applescript. If there is a more convienient way to obtain the URL of the currently active tab in Safari or to easily launch URLs I would greatly appreciate the information.

    :::python
    import os
    from subprocess import Popen, PIPE 
    from urlparse import urlparse

    # Set Default Browser
    #browser = "WebKit"
    browser = "Safari"

    # Get url address from safari / webkit
    cmd = "/usr/bin/osascript -e 'tell application \"%s\"' -e 'get URL of current tab of window 1' -e 'end tell'" % browser
    pipe = Popen(cmd, shell=True, stdout=PIPE).stdout
    url = pipe.readlines()[0].rstrip('\n')

    # Get index of current tab
    cmd = "/usr/bin/osascript -e 'tell application \"%s\"' -e 'get index of current tab of window 1' -e 'end tell'" % browser
    pipe = Popen(cmd, shell=True, stdout=PIPE).stdout
    tindex = pipe.readlines()[0].rstrip('\n')

    # Parse URL
    o = urlparse(url)
    string = ''
    if 'twitter' in o.netloc:
        if o.path != '/':
            if 'status' in o.path:
                # Open specific tweet in tweetbot
                string = "tweetbot:/%s" % o.path
            else:
                # Open user profile in tweetbot
                string = "tweetbot:///user_profile/%s" % o.path
    else:
        print "Not a Twitter URL..."

    # Open Twitter URL in Tweetbot
    if string != '':
        cmdList = []
        # Send to tweetbot, close blank safari window, switch back to original tab
        cmdList.append("""osascript -e 'tell application \"%s\" to open location \"%s\"'""" % (browser, string))
        cmdList.append("""osascript -e 'tell application \"%s\" to close current tab of window 1'""" % browser)
        cmdList.append("""osascript -e 'tell front window of application \"%s\" to set current tab to tab %s'""" % (browser, tindex))

        # Execute Commands
        for cmd in cmdList:
            os.system(cmd)

Also on [Github](https://github.com/timbueno/tinyScripts/blob/master/tweetbot.py)