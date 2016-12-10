#Final Project
##Knitting Pattern Generator

###Patterns galore!
I'm a knitter.  I knit.  A _lot_.  And sometimes I'll use existing images, convert them to bitmaps, distort as needed to suit my ratio of stitches:rows per inch, and generate a pattern.  In the past I've done this manually, but I'd like to automate the process and store the results in a database that people can browse and use.

###Requirements
The code is written using Python version 3.4 and Django 1.10.3.  Most modules are in the standard library, but you will need to install _webcolors_.  You should also make sure that _PIL_ (Pillow) is installed, because it is required for the image processing to work.

###Known issues
* File saves seem to happen in untracked threads spawned in the OS.  This can lead to attempts to create or view patterns before the files are done being written.  I've worked around this by testing to see if the file is openable before moving on to additional file-related tasks, but there's probably a better way to cope with it.

###Future development
* Establish user accounts.  This will let me move the file uploads behind a login, so that I can make reasonable attempts at assuring that it's actual human beings doing the file uploads and allow me to track the usernames of the accounts doing the uploads.
* Allow users to rotate an image during the upload.  This will save users a step in the creation of patterns for banners (e.g. to knit scarves).
* Cleanup module to delete files that don't have corresponding database records and database records that don't have corresponding images.