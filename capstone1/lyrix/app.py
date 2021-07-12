from flask import Flask, request, render_template, redirect, flash, g, session, jsonify
#from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests


from forms import LoginForm, SignupForm, LyricSearch
from models import db, connect_db, User, Favorite

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lyrix'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "landon"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
#debug = DebugToolbarExtension(app)

connect_db(app)

key = "5f372e4063fae9d0610fb5c68cf6ca0d"
API = "https://api.musixmatch.com/ws/1.1/"

CURR_USER_KEY = "curr_user"
api_url = 'https://api.musixmatch.com/ws/1.1/matcher.lyrics.get'

def get_lyrics(artist, title):
    """gets api response and send json"""
    resp = requests.get('https://api.musixmatch.com/ws/1.1/track.search', params={"apikey": "5f372e4063fae9d0610fb5c68cf6ca0d", "q_track": title, "q_artist": artist})
    res = resp.json()

    lyrics = res["message"]["body"]["lyrics"]["lyrics_body"]
    #track_id = res["message"]["body"]["lyrics"]["track_id"]

    return jsonify(
        lyrics={"artist": artist,
                "title": title,
                "songlyrics": lyrics}
    )

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def home():
    return redirect('/login')


#signing up and logging in related below

@app.route('/login', methods=["GET", "POST"])
def login():
    """allows user to login to account"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authentication(form.username.data,
                                   form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}", "success")
            return redirect('/home')
        else:
            flash("your username or password is wrong", "danger")

    return render_template('login.html', form=form)
    
    



@app.route('/signup', methods=["GET", "POST"])
def create_account():
    """creates account in DB and logs you in, and also handles errors"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = SignupForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('/signup.html', form=form)

        do_login(user)

        return redirect("/home")

    else:
        return render_template('/signup.html', form=form)




#inside app such as, Home pg, search, and favorites pg

@app.route('/home', methods=["POST", "GET"])
def home_pg():
    """shows Homepage"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = LyricSearch(enable_csrf=False)
    

    if True:
        artist = form.artist.data,
        title = form.title.data


        if artist or title:
            resp_track = requests.get(f"{API}/matcher.lyrics.get", params={"apikey": key, "q_track": title, "q_artist": artist})
            track = resp_track.json()
            #resp_artist = requests.get(f"{API}/artist.get", params={"apikey": key, "q_artist": artist}
            lyrics = track["message"]["body"]["lyrics"]["lyrics_body"]
            resp = {'lyrics': lyrics, 'artist': artist, 'title': title}
        
            return render_template('home.html', resp=resp, form=form)
        #return render_template('home.html', track=track, artist=artist, title=title, form=form)
    else:
        return render_template('err404.html')
        #resp_track = requests.get(f"{API}/matcher.lyrics.get", params={"apikey": key, "q_track": "", "q_artist": ""})
        #resp_artist = requests.get(f"{API}/artist.search", params={"apikey": key, "q_artist": ""})
        #return render_template('home.html', track=track, name=name, form=form)




@app.route('/favorites')
def fav_pg():
    return "hello world from, /favorites"


