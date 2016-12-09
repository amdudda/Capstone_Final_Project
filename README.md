#Final Project
##Knitting Pattern Generator

###Patterns galore!
I'm a knitter.  I knit.  A _lot_.  And sometimes I'll use existing images, convert them to bitmaps, distort as needed to suit my ratio of stitches:rows per inch, and generate a pattern.  In the past I've done this manually, but I'd like to automate the process and store the results in a database that people can browse and use.

###Requirements
The code is written using Python version 3.4 and Django 1.10.3.  Most modules are in the standard library, but you will also need to install _webcolors_.  You should also make sure that _PIL_ (Pillow) installed, because it is required for the image processing to work.

###Known issues
* The _views.create_new_pattern_ and _views.upload_image_ modules use `time.sleep()` to allow the system time to write image files to disk. They would be better served by spinning off processes and waiting for them to finish.