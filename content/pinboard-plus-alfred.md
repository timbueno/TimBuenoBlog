Title: Pinboard plus Alfred
Date: 2012-06-27 06:10
Tags: alfred, applescript, programming
Slug: pinboard-plus-alfred
Author: Tim Bueno
Summary: Alfred 1 script to send to pinboard

![Alfred and Pinboard](|filename|/images/Alfred_Pinboard.png)

A couple months back[^1] I quickly threw together an Applescript that allowed easy submission of links to [Pinboard](http://pinboard.in/) (my favorite bookmarking utility) from the convenience of [Alfred](http://http://www.alfredapp.com/) (the do-pretty-much-everything app launcher). If you use both and ALSO happen to use Google Chrome on a computer that runs Apple's OS X, you will **love** the convenience. A long shot, I know. 

To activate:

1. Summon Alfred via your hot key
2. Type “pin tag1 tag2 tag3 ...”
3. Press Enter
4. Growl will notify you if the submission was a success!
 
You must use tags for the script to work. Right now, I find it *convenient* that it forces me to tag my bookmarks correctly. However, I may look into removing this limitation in the future.

[Download](http://dl.dropbox.com/u/1325873/tumblr%20files/Send%20to%20Pinboard%20v1_1.alfredextension "They like me, they really like me!") 

I have included the Applescript below for anyone who wants to probe. I realize there is probably a quicker/better way to accomplish this but it works and I wrote it when I was just starting out with Applescript. 

Currently the script only works in Google Chrome. I would love to bring functionality over to Safari and that may be something I look into now that [Safari in Mountain Lion](http://www.macworld.com/article/1165466/mountain_lion_hands_on_with_safari.html) has an omnibar like Chrome's. 

I have a few of these "convenience" scripts lying around that I will try and put on Github in the coming weeks.

	:::applescript
	--****************************************
	-- Name: Chrome to Pinboard
	-- Language: Applescript
	-- Author: Tim Bueno
	-- Website: http://www.timbueno.com
	-- Date: 4/11/2011
	--****************************************

	on alfred_script(q)
	  try
		set userName to "USERNAME_GOES_HERE"
		set userPass to "PASSWORD_GOES_HERE"

		set inputt to q as text

		set tmp to splitString(inputt as text, " ")
			set AppleScript's text item delimiters to "+"
			set q to tmp as string
			set AppleScript's text item delimiters to ""
		
		tell application "Google Chrome"
			set theURL to URL of active tab of first window
			set theDesc to title of active tab of first window
		end tell
		
		set tmp to splitString(theDesc as text, " ")
		set AppleScript's text item delimiters to "+"
		set theDesc to tmp as string
		set AppleScript's text item delimiters to space
		set growlDesc to tmp as string
		set AppleScript's text item delimiters to ""
		
		set shellScript to ("curl --url \"https://" & userName & ":" & userPass & ¬
			"@api.pinboard.in/v1/posts/add?url=" & theURL & "&description=" & theDesc & "&tags=" & q & "\"")
		
		set PnbdResponse to (do shell script shellScript)
		
		if PnbdResponse contains "code=\"done\"" then
			tell application "Growl" to notify with name ¬
				"Extension Output" title ¬
				"Sent to Pinboard" description ¬
				"\"" & growlDesc & "\" has been saved!" application name ¬
				"Alfred" icon of application "Alfred"
		else
			tell application "Growl" to notify with name ¬
				"Extension Output" title ¬
				"Failed! - Sent to Pinboard" description ¬
				"There was a problem. Check your username and password." application name ¬
				"Alfred" icon of application "Alfred"
		end if
	end try
	end alfred_script

	--****************************************
	-- Split String
	--(thanks to Geert JM Vanderkelen for this code! 
	--http://geert.vanderkelen.org/post/241/)
	--****************************************
	to splitString(aString, delimiter)
		set retVal to {}
		set prevDelimiter to AppleScript's text item delimiters
		log delimiter
		set AppleScript's text item delimiters to {delimiter}
		set retVal to every text item of aString
		set AppleScript's text item delimiters to prevDelimiter
		return retVal
	end splitString


[^1]:This is *sort of* a repost from an older blog of mine. This isn't plagiarism I swear.