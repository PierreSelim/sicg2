sicg2: SurfaceImageContentGap reloaded
======================================

Research project to surface articles with most views that are lacking illustration on Wikipedia.
This is under construction and heavy rewriting.


Modules
-------

* logger: provides logger with handler already configured for stdout.
* database: provides high level methods to insert, delete, list elements from database
* bot: script to update the database
* view: script to run the webapp displaying results from the database


Configuration
-------------

You need a working configuration for `pywikibot`, or you can just
`export PYWIKIBOT2_NO_USER_CONFIG=1`
