from flask import abort
from flask.app import Flask
from flask.globals import request
from flask.templating import render_template
from flask.wrappers import Response
from sqlalchemy.dialects.postgresql.dml import insert

from conf import WEB_APP_HOST, WEB_APP_PORT
from storage import engine, Base, SessionLocal
from models import Characters, User

app = Flask(__name__, static_folder="static")

Base.metadata.create_all(engine)


# characters data adding
def check_start_data():
    db = SessionLocal()
    existed_data = db.query(Characters).all()
    if not existed_data:
        characters = [
            {
                "name": "Mario",
                "description": "Character",
                "img_path": "static/images/mario.jpeg",
                "open_ai_description": "Mario from Super Mario"
            },
            {
                "name": "Albert Einstein",
                "description": "Theoretical physicist",
                "img_path": "static/images/albert.jpeg",
                "open_ai_description": "Albert Einstein"
            }
        ]
        for character in characters:
            query = insert(Characters).values(**character)
            db.execute(query)
            db.commit()
    db.close()


@app.route('/')
def home():
    user_id = request.args.get("user_id")

    check_start_data()
    db = SessionLocal()
    characters = []
    characters_db = db.query(Characters).all()
    for character in characters_db:
        char = {
            "id": character.id,
            "name": character.name,
            "description": character.description,
            "img_path": character.img_path,
        }
        characters.append(char)
    db.close()
    return render_template("characters.html", characters=characters, user_id=user_id)


@app.route('/character_select', methods=["POST"])
def char():
    current_user = request.form.get("user_id")
    character_id = request.form.get("char_id")

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == current_user).first()
        user.character = character_id
        db.add(user)
        db.commit()
    except Exception:
        db.rollback()
        abort(500)
    finally:
        db.close()
    return Response(status=201)


if __name__ == "__main__":
    app.run(host=WEB_APP_HOST, port=WEB_APP_PORT)
