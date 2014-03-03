__author__ = 'gsibble, PaulMest'

from flask import Flask, render_template, request, make_response

from oauth2client.client import OAuth2WebServerFlow
import httplib2

APP = Flask(__name__)
APP.debug = True

host='localhost'
port=5000


import logging
logging.basicConfig()

try:       
	from secrets import CALLBACK_URL, CLIENT_ID, CLIENT_SECRET
except:
    print '''You need to create a secrets.py file in location ./coinbase_oauth2/secrets.py. It should look something like this:
__author__ = "Paul Mestemaker"
CALLBACK_URL="http://{host}:{port}/consumer_auth"              
CLIENT_ID="[Get this from Coinbase]"
CLIENT_SECRET="[Get this from Coinbase]"'''.format(host=host, port=port)
    exit()

from coinbase.config import COINBASE_AUTH_URI, COINBASE_TOKEN_URI

# SCOPE = 'all'
SCOPE = 'transactions balance'

coinbase_client = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, SCOPE, redirect_uri=CALLBACK_URL, auth_uri=COINBASE_AUTH_URI, token_uri=COINBASE_TOKEN_URI)

@APP.route('/')
def register_me():

    auth_url = coinbase_client.step1_get_authorize_url()    

    return render_template('register.jinja2', auth_url=auth_url)

@APP.route('/consumer_auth')
def receive_token():

    oauth_code = request.args['code']

    print oauth_code

    http = httplib2.Http(ca_certs='/etc/ssl/certs/ca-certificates.crt')
    # If you have difficulty with certificate validation, you can use this less secure workaround to test the rest of your code:
    # http = httplib2.Http(disable_ssl_certificate_validation=True) # Note: This is fine for development/testing, but not for production

    token = coinbase_client.step2_exchange(oauth_code, http=http)

    directions = "Use this JSON result in TEMP_CREDENTIALS (e.g. ./coinbase/config.py or ./example.py):\n{json}".format(json=token.to_json())
    print directions

    return make_response(directions.replace('\n', '<br/>'))

if __name__ == '__main__':
    print "Starting web server... Visit: http://{host}:{port}".format(host=host, port=port)
    APP.run(host=host, port=port)