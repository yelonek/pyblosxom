# vim: tabstop=4 shiftwidth=4 expandtab
"""
This plugin can help save bandwidth for low bandwidth quota sites (how
unfortunate).

This is done by outputing cache friendly HTTP header tags like Last-Modified
and ETag. These values are calculated from the first entry returned by
entryList.
"""
__author__ = "Wari Wahab pyblosxom@wari.per.sg"
__version__ = "$Id$"

def load(py, entryList):
    if entryList:
        import os, time
        # Get our first file timestamp for ETag and Last Modified
        # Last-Modified: Wed, 20 Nov 2002 10:08:12 GMT
        # ETag: "2bdc4-7b5-3ddb5f0c"
        lastModed = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(entryList[0]['mtime']))
        if ((os.environ.get('HTTP_IF_NONE_MATCH','') == '"%s"' % entryList[0]['mtime']) or
            (os.environ.get('HTTP_IF_NONE_MATCH','') == '%s' % entryList[0]['mtime']) or
            (os.environ.get('HTTP_IF_MODIFIED_SINCE','') == lastModed)):
            print 'Status: 304 Not Modified\nETag: "%s"\nLast-Modified: %s' % (
                    entryList[0]['mtime'], lastModed)
            # Enable if you want logging
            #tools.logRequest(returnCode = '304')
            raise SystemExit
        print 'ETag: "%s"' % entryList[0]['mtime']
        print 'Last-Modified: %s' % lastModed