from apiflask import APIFlask


def create_app():
    app = APIFlask(
        __name__,
        spec_path="/openapi.yaml",
        title="August Weather Data API",
        version="0.0.1",
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://august@localhost:12432/august"
    app.config["SPEC_FORMAT"] = "yaml"
    from august.model import db

    db.init_app(app)

    from august.views import api

    app.register_blueprint(api)
    return app
