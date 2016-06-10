# datamap

## Installation

Open a terminal.

### cantools

Get the framework, cantools:

  - git clone https://github.com/bubbleboy14/cantools.git

Install it:

  - cd cantools
  - python setup.py install

There's a good chance you'll need to sudo that last command, depending on how your system is set up.

### datamap

Then, go to wherever you want to install datamap:

  - cd ../myProjectsOrWhatever

And get it:

  - git clone https://github.com/antievictionmappingproject/datamap.git

And install it (this really just adds symlinks to cantools):

  - cd datamap/aemp
  - ctinit -r

## Data

Now you need to unzip your starter data:

  - unzip data.db.zip

## Server

Then run the server:

  - ctstart

It will ask you for a password. Make something up.

Open a browser and navigate to http://localhost:8080 - that's it!

## Admin

In addition to the map (at localhost:8080), there's an admin dashboard thing running on port 8002.

So check out http://localhost:8002/db in your browser if you want to mess around with the database.
It will ask you for the password you just made up.

## Model

All the tables are defined in a file called model.py. Try adding something.

## Scrapers

Say you have some big csv or something that's chalk full of too much information,
and you're too tired to read it the old fashioned way. Look no further than the
scrapers, which live in the scrapers directory. Make a new one if you want.

If you do, you can run it by adding the name of your scraper to the list on line
5 of scrape.py and hitting http://localhost:8080/scrape?scraper=whateverYourScraperIsCalled

That's it!

## Map

This runs (by default) on port 8080. If you add a new model or something, you might
want to also define some mappy behavior for it. You can do this in kinds.js, which
lives in the js/core/model directory.
