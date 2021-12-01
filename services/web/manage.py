from flask.cli import FlaskGroup

from easymail import app,db,bcrypt
from easymail.models import User

app.config.from_object("easymail.config.Config")

cli = FlaskGroup(app)
@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    cli()