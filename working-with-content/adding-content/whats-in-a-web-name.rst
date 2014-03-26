What's in a Web Name?
==========================

Individual content items on a Plone web site have discrete web
addresses. Plone creates these automatically, based on the Title that
you supply.

What's in a Web Name?
---------------------

The **Title** of content items, including folders, images, pages, etc.,
can be anything you want -- you can use any keyboard characters,
including blanks. **Titles** become part of web address for each item
you create in Plone. Web addresses, also known as URLs, are what you
type in a web browser to go to a specific location in a web site (Or,
you would click your way there), such as:

www.mysite.com/about/personnel/sally/bio

OR

www.mysite.com/images/butterflies/skippers/long-tailed-skippers

Web addresses *do* have restrictions on allowed keyboard characters, and
blanks are not allowed. Plone does a good job of keeping web addresses
correct by using near-equivalents of the **Title** that you provide, by
converting them to lowercase, and by substituting dashes for spaces and
other punctuation.

To illustrate, let's take each of these two web addresses and split them
out into their component parts:

::

    www.mysite.com/about/personnel/sally/bio
    ^ 
    website name
                   ^ 
                   a folder named About
                         ^ 
                         a folder named Personnel
                                   ^ 
                                   a folder named Sally
                                         ^ 
                                         a folder named Bio

In this example, Plone changed each folder title to lowercase, e.g.,
from Personnel to personnel. You don't have to worry about this. Plone
handles the web addressing; you just type in titles however you want.

And, for the second example:

::

    www.mysite.com/images/butterflies/skippers/long-tailed-skippers
    ^
    website name
                   ^
                   a folder named Images
                          ^
                          a folder named Butterflies
                                      ^
                                      a folder named Skippers
                                               ^
                                               a folder named Long-Tailed Skippers

This example is similar to the first, illustrating how there is a
lowercase conversion from the title of each folder to the corresponding
part of the web address. Note the case of the folder named Long-tailed
Skippers. Plone kept the dash, as that is allowed in both title and part
of the web address, but it changed the blank between the words Tailed
and Skippers to a dash, in the web address, along with the lowercase
conversion.

The web address of a given item is referred to as the **short name** in
Plone. When you use the **Rename** function, you'll see the short name
along with the title.

