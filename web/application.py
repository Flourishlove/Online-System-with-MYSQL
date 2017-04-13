# all the imports
import sys, os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

from settings import APP_STATIC

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.debug = True



@application.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        url = request.form['target_url']
        return redirect(url_for('mainpage', url=url))
    else:
        entries = []
        return render_template('index.html', entries=entries)


@application.route('/', methods=['GET'])
def mainpage():
    return render_template('index.html')

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()