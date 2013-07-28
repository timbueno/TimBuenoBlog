Title: Rolling my own automatic tweet archiver
Date: 2012-07-07 06:03
Tags: scripting, python, twitter
Slug: rolling-my-own-automatic-tweet-archiver
Author: Tim Bueno
Summary: Automatic tweet archiving in python

Working on my Tweet Archiver python script has been very fun. I have learned a fair amount about the Tweepy module and how it interfaces with Twitter's API's. Dr. Drang's [post on timezones](http://www.leancrew.com/all-this/2012/07/tweets-timestamps-time-zones-and-thinkup/) was very informative, as I was experiencing UTC time zone issues myself. Pytz made dealing with these issues nearly painless. Rest assured that I'll find an infinite number of uses for these modules in the future. 

***

The spirit of the inital conversation about archiving your tweets was clear:

1. An archive of your tweets is something worth having.
2. Twitter does not have an easy way to export your entire timeline.
3. IFTTT provides a clear, and simple way to facilitate this archival process.

But as Dr. Drang put it perfectly in his [article](http://www.leancrew.com/all-this/2012/07/archiving-tweets/):

 > The questions I need to answer now are:

> 1. Should I trust IFTTT to keep running?
> 2. Should I continue to use ThinkUp as a backup?
> 3. Should I just write my own script for archiving each day’s tweets so I don’t have to rely on ThinkUp or IFTTT?

Ignoring his comment about ThinkUp (I know next to nothing about this program), Dr. Drang brings up two interesting points. IFTTT is a great service, but for how long? If it ever does go down, will tweets that should have been archived be missed? Can I do this better myself?

I have come up with a script that replicates the original IFTTT recipe called 'autoTweetArchiver.py'. The code has been pasted below and is available on [Github](https://github.com/timbueno/SimpleTweetArchiver).

    :::python
    # autotweetArchiver.py
    #
    # Quickly archive your tweets to a plain text file.
    # Attach this script to a cron task and automatically
    # archive your tweets at any interval you choose!
    #
    # Created by: Tim Bueno
    # Website: http://www.timbueno.com
    #
    # USAGE: python autoTweetArchiver.py {USERNAME} {LOG_FILE} {TIMEZONE}
    #
    # EXAMPLE: python autoTweetArchiver.py timbueno /Users/timbueno/Desktop/logDir/timbueno_twitter.txt US/Eastern
    # EXAMPLE: python autoTweetArchiver.py BuenoDev /Users/timbueno/Desktop/logDir/buenodev_twitter.txt US/Eastern
    #
    # TODO:

    import tweepy
    import codecs
    import os
    import sys
    import pytz


    # USER INFO GATHERED FROM COMMAND LINE
    theUserName = sys.argv[1]
    archiveFile = sys.argv[2]
    homeTZ = sys.argv[3]
    homeTZ = pytz.timezone(homeTZ)

    # lastTweetId file location
    idFile = theUserName + '.tweetid'
    pwd = os.path.dirname(__file__) # get script directory
    idFile = os.path.join(pwd, idFile) # join dir and filename
    # Instantiate time zone object
    utc = pytz.utc
    # Create Twitter API Object
    api = tweepy.API()

    # helpful variables
    status_list = [] # Create empty list to hold statuses
    cur_status_count = 0 # set current status count to zero

    print "- - - - - - - - - - - - - - - - -"
    print "autoTweetArchiver.py"

    if os.path.exists(idFile):
        # Get most recent tweet id from file
        f = open(idFile, 'r')
        idValue = f.read()
        f.close()
        idValue = int(idValue)
        print "- - - - - - - - - - - - - - - - -"
        print "tweetID file found! "
        print "Latest Tweet ID: " +str(idValue)
        print "Gathering unarchived tweets... "
        
        # Get first page of unarchived statuses
        statuses = api.user_timeline(count=200, include_rts=True, since_id=idValue, screen_name=theUserName)
        # Get User information for display
        if statuses != []:
            theUser = statuses[0].author
            total_status_count = theUser.statuses_count

        while statuses != []:
            cur_status_count = cur_status_count + len(statuses)
            for status in statuses:
                status_list.append(status)
                
            theMaxId = statuses[-1].id
            theMaxId = theMaxId - 1
            # Get next page of unarchived statuses
            statuses = api.user_timeline(count=200, include_rts=True, since_id=idValue, max_id=theMaxId, screen_name=theUserName)
            
    else:
        # Request first status page from twitter
        statuses = api.user_timeline(count=200, include_rts=True, screen_name=theUserName)
        # Get User information for display
        theUser = statuses[0].author
        total_status_count = theUser.statuses_count
        print "- - - - - - - - - - - - - - - - -"
        print "No tweetID file found..."
        print "Creating a new archive file"
        print "- - - - - - - - - - - - - - - - -"

        while statuses != []:
            cur_status_count = cur_status_count + len(statuses)
            for status in statuses:
                status_list.append(status)
            
            # Get tweet id from last status in each page
            theMaxId = statuses[-1].id
            theMaxId = theMaxId - 1
            
            # Get new page of statuses based on current id location
            statuses = api.user_timeline(count=200, include_rts=True, max_id=theMaxId, screen_name=theUserName)
            print "%d of %d tweets processed..." % (cur_status_count, total_status_count)

        print "- - - - - - - - - - - - - - - - -"
        # print "Total Statuses Retrieved: " + str(len(status_list))
        print "Writing statuses to log file:"

    #Write tweets to archive
    if status_list != []:
        print "Writing tweets to archive..."
        print "Archive file:"
        print archiveFile
        print "- - - - - - - - - - - - - - - - -"
        f = codecs.open(archiveFile, 'a', 'utf-8')
        for status in reversed(status_list):
            theTime = utc.localize(status.created_at).astimezone(homeTZ)
            # Format your tweet archive here!
            f.write(status.text + '\n')
            f.write(theTime.strftime("%B %d, %Y at %I:%M%p\n"))
            f.write('http://twitter.com/'+status.author.screen_name+'/status/'+str(status.id)+'\n')
            f.write('- - - - - \n\n')
        f.close()

        # Write most recent tweet id to file for reuse
        print "Saving last tweet id for later..."
        f = open(idFile, 'w')
        f.write(str(status_list[0].id))
        f.close()

    if status_list == []:
        print "- - - - - - - - - - - - - - - - -"
        print "No new tweets to archive!"
    print "Total Statuses Retrieved: " + str(len(status_list))
    print "Finished!"
    print "- - - - - - - - - - - - - - - - -"

To run the script, clone the Github repository or copy and paste the code into your favorite text editor and save it to something like 'autoTweetArchiver.py'.  Make sure you have the required dependencies installed, then execute it with: 

    :::bash
    python autoTweetArchiver.py {USERNAME} {LOG_FILE} {TIMEZONE}

Replace the bracketed arguments with your personal details. Make sure it looks something like this:

    :::bash
    python autoTweetArchiver.py timbueno /logDir/twitter.txt US/Eastern


On first execution the script will

1. Grab all of your previous tweets (up to 3,200)
2. Write these tweets to the specified text file
3. Create a 'username.tweetid' file in the same directory as the script

Upon successive executions the script will

1. Open the 'username.tweetid' file and extract the most recent tweet archived
2. Grab all tweets that have happened since last execution
3. Append these new tweets to the end of the specified text file
4. Update the 'username.tweetid' file for next execution

The 'username.tweetid' file simply contains the ID number twitter gives every tweet. I use this value to gather all tweets between last execution and the current one.

***
The third input argument, '{TIMEZONE}' must be formatted corectly or the script will fail. Tweepy's status object contains a python datetime object set to UTC time. The user must provide their timezone to localize the archive to their local time. For a list of available timezones head over [here](https://github.com/timbueno/SimpleTweetArchiver/blob/master/timezones.txt). If you're timezone is not listed there, let me know and I can add it.
***
Of course, no one wants to have to manually run this script. The beauty of the IFTTT recipe is that they handle the automation for you.

There are many different ways that the executions of this script can be automated, although none are as simple as using IFTTT. [Macdrifter](http://www.macdrifter.com/2012/02/fever-reader-review/) uses [Keyboard Maestro](http://www.keyboardmaestro.com/main/) for all of his automation tasks. This method is great for those of you wishing to run this script automatically on your local machine. Scripts can be set to run at any interval, with a very simple setup.

![Automation with Keyboard Maestro](|filename|/images/autotweetarchiver_keyboardmaestro.png)

Apple provides the program [launchd](http://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man1/launchctl.1.html), however I have not had any experience with it, so I will not be explaining how to set this up.

Finally, my preferred method is to have [cron](http://en.wikipedia.org/wiki/Cron) handle the scheduling and automation. I have edited 'crontab' (with 'crontab -e') on my remote server with a line like this: 

    :::bash
    * * * * * python /home/blog/scripts/SimpleTweetArchiver/autoTweetArchiver.py timbueno  /path/to/archive/Dropbox/logs/timbueno_twitter.txt US/Eastern

I have placed the 'timbueno_twitter.txt' archive text file in the Dropbox folder on my server. Saving the archive file to Dropbox allows me to access the archive from anywhere in the world. 

The first five characters in the cronjob ('* * * * * ') tell cron to execute the following script every minute. This isn't very practical as it is unnecessary to update the archive that often. Below I have included common cron schedules:

<pre>
Run once a year, midnight, Jan. 1st
0 0 1 1 *

Run once a month, midnight, first of month
0 0 1 * *

Run once a week, midnight on Sunday
0 0 * * 0

Run once a day, midnight
0 0 * * *

Run once an hour, beginning of hour
0 * * * *
</pre>

Cron's syntax can be confusing so if you get stuck, head over [here](http://www.abunchofutils.com/utils/developer/cron-expression-helper/) for some help.

***

You can archive multiple twitter accounts automatically as well. Add additional jobs to your 'crontab' to make it happen. Make sure each log file is named differently, or you will append the tweets of multiple twitter usernames to the same logfile (maybe you want that, go for it!).

***

The past few days have been an enjoyable learning experience for me, and I hope someone somewhere can take advantage of these scripts. I'll continue to work on them as time allows. As the source is freely available on Github I welcome everyone to pick apart my code, add features, log styles, and fix any pesky bugs you may find.

I've got more ideas for python scripting coming down the pipeline as well so check back here soon! test