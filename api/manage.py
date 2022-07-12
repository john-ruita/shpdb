from flask.cli import FlaskGroup
from project import app, db, Shapefile

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    Shapefile.__table__.drop(db.engine)
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()
