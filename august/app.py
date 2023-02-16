from pathlib import Path

import click
from apiflask import APIFlask
from flask.cli import FlaskGroup


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

    @app.cli.command()
    def create_db():
        """Create DB from models"""
        db.create_all()

    @app.cli.command()
    @click.argument(
        "directory", type=click.Path(exists=True, path_type=Path, file_okay=False)
    )
    def import_weather_data(directory: Path):
        """Import weather data"""
        from august.libs.importer import WeatherDataImporter

        click.echo("Beginning weather data import")
        importer = WeatherDataImporter(directory)
        count = importer.run()
        click.echo(
            f"Weather data import complete. {count} records imported or updated."
        )

    @app.cli.command()
    def calculate_summary_data():
        """Calculate summary weather data"""
        from august.libs.stats import calculate_summary_data

        calculate_summary_data()

    return app


cli = FlaskGroup(create_app=create_app)
