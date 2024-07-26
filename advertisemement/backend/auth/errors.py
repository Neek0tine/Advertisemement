from flask import redirect, url_for
from . import app

@app.errorhandler(400)
def badrequest(e):
    return redirect(url_for('dashboard'))


# @app.errorhandler(403)
# def forbidden(e):
#     return render_template('tweets_null.html'), 403


# @app.errorhandler(500)
# def serverError(e):
#     return redirect(url_for('dashboard')), 500


# @app.errorhandler(Exception)
# def defaultHandler(e):
#     return render_template('tweets_null.html')