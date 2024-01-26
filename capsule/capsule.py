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
# from time import sleep
import asyncio
from pyppeteer import launch
from capsule.auth import login_required
from capsule.db import get_db

bp = Blueprint("capsule", __name__)


async def scrape_yt(song_name):
    # scrap the youtube for the song
    # return the link of the song
    # if the song is not found return "None"
    # else return the link
    url = "https://www.youtube.com/results?search_query=" + song_name
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url, {"waitUntil": "domcontentloaded"})
    await page.content()
    title = await page.evaluate("document.title")
    print(f"Title: {title}")

    all_links = await page.querySelectorAll("a")
    print(f"Found {len(all_links)} links")

    for link in all_links:
        href = (await link.getProperty("href")).jsonValue()
        if "?v=" in href:
            print(href)
            href
            break
    await browser.close()
    # if embed_link:
    #     return embed_link
    # else:
    #     return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


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
            # print(__name__)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            asyncio.get_event_loop().run_until_complete(scrape_yt(song_name))
            
            # print(embed_link)
            db = get_db()
            db.execute(
                "INSERT INTO capsule (content, song_name, user_id) VALUES (?, ?, ?)",
                (content, song_name, g.user["id"]),
            )
            db.commit()
            flash("Capsule created successfully")
            return redirect(url_for("capsule.index"))
    return render_template("capsule/create.html")

