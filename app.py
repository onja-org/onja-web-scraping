from flask import Flask
from routes.company_routes import company_bp

app = Flask(__name__)

app.register_blueprint(company_bp)

if __name__ == '__main__':
    app.run(debug=True)