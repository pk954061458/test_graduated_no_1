from flask import Flask, request
from backend.routes.auth import auth_bp
from backend.utils.logger import request_logger

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.after_request
def after_request(response):
    request_logger(request, response)
    return response

if __name__ == '__main__':
    app.run(debug=True)