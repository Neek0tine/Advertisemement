from backend.auth import app, db
import os
# from backend.auth import defaultHandler

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.config['TRAP_HTTP_EXCEPTIONS'] = True
    app.run(host="127.0.0.1", port=int(os.environ.get('PORT', 5030)), debug=True, threaded=True)