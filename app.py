# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    if req.get("result").get("action") != "my-timetable":
        return {}
    baseurl = "http://abhishek7.pythonanywhere.com/days/"
    number = makeYqlQuery(req)
    if number is None:
        return {}
    yql_url = baseurl + number
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    number = parameters.get("number-integer")
    if number is None:
        return None

    return number


def makeWebhookResult(data):

    speech = "Today is "+ data.get(day_name)+"day"+\
    		"Today's Schedule: " + \
    		"slot 1: " + data.get('slot_1') + \
    		"slot 2: " + data.get('slot_2') + \
    		"slot 3: " + data.get('slot_3') + \
    		"slot 4: " + data.get('slot_4') + \
    		"slot 5: " + data.get('slot_5') + \
   			"slot 6: " + data.get('slot_6')

    print("Response:")
    print(speech)

    return {
        "speech": "5624",
        "displayText": "1234",
        # "data": data,
        # "contextOut": [],
        "source": "my-timetable"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
