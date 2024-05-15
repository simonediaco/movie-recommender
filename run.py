from flask import Flask
from tmdbv3api import TMDb

tmdb = TMDb()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '3cb5d394e8eb3ae4351dc3c13249a5a9'
    app.config['TMDB_API_KEY'] = '3cb5d394e8eb3ae4351dc3c13249a5a9'

    tmdb.api_key = app.config['TMDB_API_KEY']
    tmdb.language = 'en'
    tmdb.debug = True

    # Registrazione delle blueprint
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
