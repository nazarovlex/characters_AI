import requests
from flask import abort, logging
from flask.app import Flask
from flask.globals import request
from flask.templating import render_template
from flask.wrappers import Response
from sqlalchemy.dialects.postgresql.dml import insert
from conf import WEB_APP_HOST, WEB_APP_PORT, AMPLITUDE_API_KEY
from storage import engine, Base, SessionLocal
from models import Characters, User

app = Flask(__name__, static_folder="static")

Base.metadata.create_all(engine)


# Amplitude events
async def track_event(user_id, event_type, properties=None):
    url = f"https://api.amplitude.com/2/httpapi"
    data = {
        "api_key": AMPLITUDE_API_KEY,
        "events": [
            {
                "user_id": str(user_id),
                "event_type": event_type,
                "event_properties": properties
            }
        ]
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error("Failed to track event: %s", e)

# characters data adding
async def check_start_data():
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
async def home():
    user_id = request.args.get("user_id")

    await check_start_data()
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
async def char():
    current_user = request.form.get("user_id")
    character_id = request.form.get("char_id")

    await track_event(current_user, 'character_select', {'character_id': character_id})

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
