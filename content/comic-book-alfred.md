Title: Comic Book Previews
Date: 2013-4-01 10:20
Tags: alfred, python
Slug: comic-book-alfred
Author: Tim Bueno
Summary: Alfred workflow to gather the latest comic book releases

[Alfred 2](http://www.alfredapp.com/) came out a few weeks ago and I am loving the upgrade. The new workflow system is amazingly powerful and some of the things people are coming up with are great.

I have been playing around with building my own workflows since the release. Alfred's workflow system is very flexible in that it allows you to use whatever scripting language you are most comfortable with to generate the [Feedback XML](http://www.alfredforum.com/topic/5-generating-feedback-in-workflows/) necessary for displaying your content in the Alfred pop-up. My language of choice is once again Python. [Daniel Shannon](http://daniel.sh/alfred.html) has written alp, a python module intended speed up the development of Alfred workflows written in Python and it works very well.

Each week I check [PreviewsWorld](http://www.previewsworld.com/Home/1/1/71/952) to see the comics that are coming out. I then add comics that I am interested in to my calendar. I've written an Alfred workflow to speed up this process.

![Next Weeks Comics](|filename|/images/PreviewsComics/comicsnext.png)

The workflow takes two inputs: *this* and *next*. As you would expect, *this* returns this weeks comics while *next* returns next weeks comics. 

Actioning on a publisher will take you to a list of the comics that publisher is releasing that week. 

![Image Comics](|filename|/images/PreviewsComics/comicsimage.png)

Actioning on a comic book will bring you to that comics description page on PreviewsWorld. Even more useful however is what happens when you hold command while actioning. 

When command is held while actioning on a comic Fantastical is opened with the text field pre-populated with the comic and the date. If Fantastical is not installed, nothing will happen.

You can see the source and keep updated on the project over on [Github](https://github.com/timbueno/BuenoAlfred). I encourage you to look into my use of autocomplete to assist in moving between pages in the workflow.

Writing this script has been a fun learning experience and I hope to make a few more of these workflows as I get the time. Let me know if you like it.