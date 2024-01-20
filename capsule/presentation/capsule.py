# create a blueprint for the capsule presentation
# this blueprint will be used to create the routes for the capsule presentation
# we will take a content from user and a name of a song and we will create a capsule
# then we will fetch th song from the youtube using beautiful soup will save the link of the song in the database
# after 24 hours we will send the capsule to the user(displays the song and the content)

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)

from capsule.auth.auth import login_required
from capsule.database.db import get_db

import time
# import threading
from bs4 import BeautifulSoup
import requests

bp = Blueprint("capsule", __name__)

def scrap_yt(song_name):
    try:
        # scrap the youtube for the song
        # return the link of the song
        # if the song is not found return None
        # else return the link
        url = "https://www.youtube.com/results?search_query=" + song_name
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        video_link = soup.find("a", {"class": "yt-simple-endpoint"})["href"]
        embedded_link = f"https://www.youtube.com/embed{video_link}"
        return embedded_link
    except Exception as e:
        print(e)
        return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

@bp.route("/")
@login_required
def index():
    # About the project and IEEE
    # button for create capsule
    return render_template("capsule/index.html")

@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    # create a capsule
    # take the content and the song name from the user
    # create a capsule and save it in the database
    # then redirect to the home page
    if request.method == "POST":
        content = request.form["content"]
        song_name = request.form["song_name"]
        error = None

        if not content:
            error = "Content is required."
        elif not song_name:
            error = "Song name is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO capsule (content, song_name, user_id) VALUES (?, ?, ?)",
                (content, song_name, g.user["id"]),
            )
            db.commit()
            flash("Capsule created successfully")
            return redirect(url_for("capsule.index"))
    return render_template("capsule/create.html")


@bp.route("/show_capsule")
@login_required
def show_capsule():
    # show the capsules of the user
    # if the user is not logged in redirect to the login page
    # else show the capsules of the user
    surprise_user(g.user['id'])
    return render_template("capsule/show.html")

def surprise_user(user_id):
    # send the capsule to the user
    # get the capsule from the database
    # send the capsule to the user
    db = get_db()
    capsule = db.execute(
        'SELECT * FROM capsule WHERE user_id = ?',
        (user_id,)
    ).fetchone()
    if capsule:
        embed_link = scrap_yt(capsule['song_name'])
        db.execute(
            'UPDATE capsule SET embed_link = ? WHERE id = ?',
            (embed_link, capsule['id'])
        )
        db.commit()


    # thread = threading.Thread(target=surprise_user, args=(g.user['id'],))
    # thread.start()
    # return redirect(url_for("capsule/show.html"))