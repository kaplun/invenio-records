## $Id$
##
## This file is part of the CERN Document Server Software (CDSware).
## Copyright (C) 2002, 2003, 2004, 2005 CERN.
##
## The CDSware is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## The CDSware is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.  
##
## You should have received a copy of the GNU General Public License
## along with CDSware; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

import sys
import sre
import MySQLdb

from cdsware.config import weburl,cdsname,cdslang,cachedir,cdsnameintl

def index(req, c=cdsname, as="0", verbose="1", ln=cdslang):
    "Display search interface page for collection c by looking in the collection cache."
    from cdsware.webpage import page, create_error_box
    from cdsware.webuser import getUid, page_not_authorized
    from cdsware.messages import wash_language, gettext_set_language
    from cdsware.search_engine import get_colID, get_coll_i18nname
    # wash params:
    try:
        as = int(as)
    except:
        as = 0
    try:
        verbose = int(verbose)
    except:
        verbose = 1
    if type(c) is list:
        c = c[0]
    ln = wash_language(ln)

    _ = gettext_set_language(ln)

    # get user ID:
    try:
        uid = getUid(req)
        if uid == -1:
            return page_not_authorized(req, "../")
    except MySQLdb.Error, e:
        return page(title=_("Internal Error"),
                    body = create_error_box(req, verbose=verbose, ln=ln),
                    description="%s - Internal Error" % cdsname, 
                    keywords="%s, CDSware, Internal Error" % cdsname,
                    language=ln,
                    urlargs=req.args)
    # start display:
    req.content_type = "text/html"
    req.send_http_header()
    # deduce collection id:
    colID = get_colID(c)
    if type(colID) is not int:
         return page(title=_("Collection %s Not Found") % c,
                     body=_("<p>Sorry, collection <strong>%s</strong> does not seem to exist. "
                            "<p>You may want to start browsing from <a href=\"%s\">%s</a>.") % (c, "%s?ln=%s" % (weburl, ln), cdsnameintl[ln]),
                     description="%s - Not found: %s " % (cdsname, c),
                     keywords="%s, CDSware" % cdsname,
                     uid=uid,
                     language=ln,
                     urlargs=req.args)
    # display collection interface page:
    try:
        fp = open("%s/collections/%d/navtrail-as=%d-ln=%s.html" % (cachedir, colID, as, ln), "r")
        c_navtrail = fp.read()
        fp.close()
        fp = open("%s/collections/%d/body-as=%d-ln=%s.html" % (cachedir, colID, as, ln), "r")
        c_body = fp.read()
        fp.close()
        fp = open("%s/collections/%d/portalbox-tp-ln=%s.html" % (cachedir, colID, ln), "r")
        c_portalbox_tp = fp.read()
        fp.close()
        fp = open("%s/collections/%d/portalbox-te-ln=%s.html" % (cachedir, colID, ln), "r")
        c_portalbox_te = fp.read()
        fp.close()
        fp = open("%s/collections/%d/portalbox-lt-ln=%s.html" % (cachedir, colID, ln), "r")
        c_portalbox_lt = fp.read()
        fp.close()
        fp = open("%s/collections/%d/portalbox-rt-ln=%s.html" % (cachedir, colID, ln), "r")
        c_portalbox_rt = fp.read()
        fp.close()
        fp = open("%s/collections/%d/last-updated-ln=%s.html" % (cachedir, colID, ln), "r")
        c_last_updated = fp.read()
        fp.close()
        if c == cdsname:
            title = cdsnameintl[ln]
        else:
            title = get_coll_i18nname(c, ln)
            
        return page(title=title,
                    body=c_body,
                    navtrail=c_navtrail,
                    description="%s - %s" % (cdsname, c),
                    keywords="%s, CDSware, %s" % (cdsname, c),
                    uid=uid,
                    language=ln,
                    urlargs=req.args,
                    cdspageboxlefttopadd=c_portalbox_lt,
                    cdspageboxrighttopadd=c_portalbox_rt,
                    titleprologue=c_portalbox_tp,
                    titleepilogue=c_portalbox_te,
                    lastupdated=c_last_updated)                    
    except:        
        if verbose >= 9:
            req.write("<br>c=%s" % c)
            req.write("<br>as=%s" % as)        
            req.write("<br>ln=%s" % ln)        
            req.write("<br>colID=%s" % colID)
            req.write("<br>uid=%s" % uid)
        return page(title=_("Internal Error"),
                    body = create_error_box(req, ln=ln),
                    description="%s - Internal Error" % cdsname, 
                    keywords="%s, CDSware, Internal Error" % cdsname,
                    uid=uid,
                    language=ln,
                    urlargs=req.args)
         
    return "\n"    
