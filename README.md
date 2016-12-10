#Software Development Capstone Final Project
##Knitting Pattern Generator

###Patterns galore!
I'm a knitter.  I knit.  A _lot_.  And sometimes I'll use existing images, convert them to bitmaps, distort as needed to suit my ratio of stitches:rows per inch, and generate a pattern.  In the past I've done this manually, but I'd like to automate the process and store the results in a database that people can browse and use.

###Requirements
The code is written using Python version 3.4 and Django 1.10.3.  Most modules are in the standard library, but you will need to install _webcolors_.  You should also make sure that _PIL_ (Pillow) is installed, because it is required for the image processing to work.

###Known issues
* File saves seem to happen in untracked threads spawned in the OS.  This can lead to attempts to create or view patterns before the necessary files are done being written.  I've worked around this by testing to see if the file is openable before moving on to additional file-related tasks, but there's probably a better way to cope with it.

###Future development
* Change the name of the site; "Knit Knacks" is used by __lots__ of people.  "Patternmaker's Guild" doesn't turn up much in the way of knitting-related stuff, so that might be usable.
* Establish user accounts.  This will let me move the file uploads behind a login, so that I can make reasonable attempts at assuring that it's actual human beings doing the file uploads and allow me to track the usernames of the accounts doing the uploads.
* Allow users to rotate and/or resize an image during the upload.  This will save users some steps in the creation of patterns for banners (e.g. to knit scarves) or getting an image of appropriate pixel width.
* Generate cross-stitch patterns. This involves tweaking the current pattern generation module into a new module for cross-stitch and coding a view to create the grid layout.
* Write a cleanup module to delete files that don't have corresponding database records and database records that don't have corresponding images.
* Search functionality, so users can search by number of colors, image size, or a particular gauge.