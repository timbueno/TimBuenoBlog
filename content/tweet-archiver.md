Title: Tweet Archiver
Link: https://github.com/timbueno/SimpleTweetArchiver
Date: 2012-07-05 11:39
Slug: tweet-archiver
Author: Tim Bueno
Summary: Simple plain text tweet archiver

Earlier this week I became interested in a discussion floating around the internet dealing with a very cool IFTTT recipe. [IFTTT](http://ifttt.com/) allows for easy scripting between some of your favorite web services. While the functionality is certaintly limited, creative individuals are cooking up cool uses for the service. This [particular recipe](http://ifttt.com/recipes/37991) archives every status update you send to twitter to an extremely light-weight plain text file. The plain text format is great as it will always be readable and is not bound to any particular service or app.

The only issue with the IFTTT  recipe is that it will not archive any tweet that you posted *before* setting the recipe up, limiting its usefulness. Both [Brett Terpstra](https://twitter.com/ttscoff/status/220860115467763712) and [Dr. Drang](http://www.leancrew.com/all-this/2012/07/archiving-tweets/) created excellent solutions, but they assume that you have access to your old tweets in other locations, such as [ThinkUp](http://thinkupapp.com/). While ThinkUp is nice, its not very practical to set up if you are only interested in using it once.

Today, I wrote a quick python script that grabs every tweet you have ever posted, and writes it to a file in the same format as the IFTTT recipe mentioned earlier. You can modify the output to fit any custom style fairly easily as well.

My current 'twitter.txt' archive file has each tweet formatted like this:
<pre>
RT @kanyewest: I love me
July 31, 2010 at 05:57PM
http://twitter.com/timbueno/20008539872
- - - - -

</pre>

You can find the Github page [here](https://github.com/timbueno/SimpleTweetArchiver). I have also posted the code (as it stands right now) below:

    :::python
    # tweetArchiver.py
    #
    # Quickly archive your tweets to a plain text file.
    #
    # This script is limited to retrieving only your
    # 3,200 most recent tweets (you have twitter
    # to thank for that)
    #
    # Created by: Tim Bueno
    # Website: http://www.timbueno.com
    #
    # USAGE: python tweetArchiver.py

    import tweepy
    import codecs
    import pytz

    utc = pytz.utc

    # Archive file location
    archiveFile = "/Users/timbueno/Desktop/logDir/twitter.txt"
    theUserName = 'timbueno'
    homeTZ = pytz.timezone('US/Eastern')

    # Create Twitter API Object
    api = tweepy.API()

    # helpful variables
    status_list = [] # Create empty list to hold statuses
    cur_status_count = 0 

    # Request first status page from twitter
    statuses = api.user_timeline(count=200, include_rts=True, screen_name=theUserName)
    # Get User information for display
    theUser = statuses[0].author
    total_status_count = theUser.statuses_count
    print "- - - - - - - - - - - - - - - - -"
    print "- Archiving "+theUser.name+"'s tweets"
    print "- Archive file:"
    print "- " + archiveFile
    print "-"
    print "- http://www.timbueno.com"
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
    print "Total Statuses Retrieved: " + str(len(status_list))
    print "Writing statuses to log file:"

    f = codecs.open(archiveFile, 'a', 'utf-8')
    for status in reversed(status_list):
        theTime = utc.localize(status.created_at).astimezone(homeTZ)
        f.write(status.text + '\n')
        f.write(theTime.strftime("%B %d, %Y at %I:%M%p\n"))
        f.write('http://twitter.com/'+status.author.screen_name+'/status/'+str(status.id)+'\n')
        f.write('- - - - - \n\n')

    f.close()

    print "Finished!"
    print "- - - - - - - - - - - - - - - - -"

The "status_list" contains any number of tweepy Status object. This list is looped over and each status object is available to process in any way you choose. The code to where this data is formatted begins on line 57. The status object has a **ton** of content about each individual tweet. I've included an example structure of the status object below 

    :::python
    {
     'contributors': None, 
     'truncated': False, 
     'text': '@ERCourtney Working with anyone\u2019s code but your own is a very frustrating experience most of the time. I hear ya.',
     'in_reply_to_status_id': None,
     'id': 220264265720930304,
     '_api': <tweepy.api.API object at 0x1096afc10>,
     'author': <tweepy.models.User object at 0x10990ae10>,
     'retweeted': False,
     'coordinates': None,
     'source': 'My Top Followers in 2010',
     'in_reply_to_screen_name': None,
     'id_str': '21041793667694593',
     'retweet_count': 0,
     'in_reply_to_user_id': None,
     'favorited': False,
     'source_url': 'http://mytopfollowersin2010.com', 
     'user': <tweepy.models.User object at 0x10990ae10>,
     'geo': None, 
     'in_reply_to_user_id_str': None, 
     'created_at': datetime.datetime(2012, 7, 3, 21, 14, 27), 
     'in_reply_to_status_id_str': None, 
     'place': None
    }

...and the tweepy User object for completness. 

    :::python
    {
     'follow_request_sent': False, 
     'profile_use_background_image': True, 
     'id': 132728535, 
     '_api': <tweepy.api.api object="" at="" xxxxxxx="">, 
     'verified': False, 
     'profile_sidebar_fill_color': 'C0DFEC', 
     'profile_text_color': '333333', 
     'followers_count': 80, 
     'protected': False, 
     'location': 'Seoul Korea', 
     'profile_background_color': '022330', 
     'id_str': '132728535', 
     'utc_offset': 32400, 
     'statuses_count': 742, 
     'description': "Cars, Musics, Games, Electronics, toys, food, etc... I'm just a typical boy!",
     'friends_count': 133, 
     'profile_link_color': '0084B4', 
     'profile_image_url': 'http://a1.twimg.com/profile_images/1213351752/_2_2__normal.jpg',
     'notifications': False, 
     'show_all_inline_media': False, 
     'geo_enabled': True, 
     'profile_background_image_url': 'http://a2.twimg.com/a/1294785484/images/themes/theme15/bg.png',
     'screen_name': 'jaeeeee', 
     'lang': 'en', 
     'following': True, 
     'profile_background_tile': False, 
     'favourites_count': 2, 
     'name': 'Jae Jung Chung', 
     'url': 'http://www.carbonize.co.kr', 
     'created_at': datetime.datetime(2010, 4, 14, 1, 20, 45), 
     'contributors_enabled': False, 
     'time_zone': 'Seoul', 
     'profile_sidebar_border_color': 'a8c7f7', 
     'is_translator': False, 
     'listed_count': 2
    }

Either clone my Github repository locally, or copy and paste the scripts code from above and save it to a file called something like 'tweetArchiver.py'. Make sure you have [tweepy](https://github.com/tweepy/tweepy) and [pytz](http://pytz.sourceforge.net/) (for timezones correction) installed as well. It's easy if you have pip installed:

    :::bash
    pip install tweepy
    pip install pytz

Edit the 'archiveFile' variable at the top of the script to the file location you want to be written to:

    :::python
    archiveFile = "/Users/timbueno/Desktop/logDir/twitter.txt"

Execute my script like so:
    :::bash
    python tweetArchiver.py

After the log file is created you can point the aforementioned IFTTT recipe to the log file for further appending each time you tweet!

I cooked this up earlier today so there very well could be some bugs. Feel free to let me know of any you find!

**Edit:** As Brett Terpsta has [pointed out](https://twitter.com/ttscoff/status/221089856728743937), my script is limited to around 3200 statuses. The heavier twitter users, and the not so distant future me, will be over this limit. So if you are under 3200 tweets, now is the time to begin archiving!

**Edit 2:**  [Dr. Drang weighed in](https://twitter.com/drdrang/status/221243066588213248) on my code as well. My original implementation required the user to authenticate their twitter acount with my application. This ultimately was not necessary and I have removed it from the code above and have pushed the changes to Github.

**Edit 3:** I hope this is the last edit! I've updated the tweetArchiver.py script once again to adjust for timezones. However, this did add a dependencey on the 'pytz' module. But if its good enough for Dr. Drang, its good enough for me!