import connexion


def create_app():
    connexion_app = connexion.FlaskApp(__name__, specification_dir="openapi/")
    connexion_app.add_api("weather_api.yaml")
    app = connexion_app.create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://august@localhost:12432/august"
    from august.model import db

    db.init_app(app)

    from august.views import api

    app.register_blueprint(api)
    return app
