# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2011 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""WebMessage Forms"""

from string import strip
from datetime import datetime
from invenio.webmessage_config import CFG_WEBMESSAGE_ROLES_WITHOUT_QUOTA, \
                                      CFG_WEBMESSAGE_STATUS_CODE, \
                                      CFG_WEBMESSAGE_SEPARATOR
from invenio.config import CFG_SITE_LANG, \
                           CFG_WEBMESSAGE_MAX_NB_OF_MESSAGES, \
                           CFG_WEBMESSAGE_MAX_SIZE_OF_MESSAGE

from invenio.sqlalchemyutils import db
from invenio.websession_model import User, Usergroup
from invenio.webmessage_model import MsgMESSAGE, UserMsgMESSAGE
from invenio.webinterface_handler_flask_utils import _
from flask.ext.wtf import Form
from invenio.wtforms_utils import InvenioBaseForm, FilterForm, DateTimePickerWidget, FilterTextField
from wtforms import DateTimeField, BooleanField, TextField, TextAreaField, \
                    PasswordField, validators, HiddenField


class CollectionForm(InvenioBaseForm):
    id = HiddenField()
    name = TextField(_('Name'))  
    dbquery = TextField(_('Query'))

