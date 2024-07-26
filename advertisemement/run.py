from backend.auth import app, db
from backend.auth.errors import badrequest
import os
# from backend.auth import defaultHandler

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.config['TRAP_HTTP_EXCEPTIONS'] = True
    app.run(host="127.0.0.1", port=int(os.environ.get('PORT', 1337)), debug=True, threaded=True)
    app.register_error_handler(Exception, badrequest)