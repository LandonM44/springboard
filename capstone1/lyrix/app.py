from flask import Flask, request, render_template, redirect, flash, g, session, jsonify
#from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests


from forms import LoginForm, SignupForm, LyricSearch, AddFavSong
from models import UserFavorites, db, connect_db, Users, Favorite

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


def get_chart_artists():
    """gets api response and send json"""
    resp = requests.get('https://api.musixmatch.com/ws/1.1/chart.tracks.get', params={"apikey": "5f372e4063fae9d0610fb5c68cf6ca0d", "page": 1, "page_size": 16, "format": "json"})
    res = resp.json()

    top_charts = res["message"]["body"]["track_list"]
    #track_id = res["message"]["body"]["lyrics"]["track_id"]

    return top_charts

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = Users.query.get(session[CURR_USER_KEY])

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
        user = Users.authentication(form.username.data,
                                   form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}", "success")
            return redirect('/home')
        else:
            flash("your username or password is wrong", "danger")

    return render_template('login.html', form=form)
    
    
@app.route('/logout')
def logout():

    do_logout()

    flash("You are logged out", "success")
    return redirect("/login")


@app.route('/signup', methods=["GET", "POST"])
def create_account():
    """creates account in DB and logs you in, and also handles errors"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = SignupForm()

    if form.validate_on_submit():
        try:
            user = Users.signup(
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

    

    form = LyricSearch()
    

    if form.validate_on_submit():
        artist = form.artist.data,
        title = form.title.data

        
        if artist or title:
            #requests to msuixmatch api
            resp_lyrics = requests.get(f"{API}/matcher.lyrics.get", params={"apikey": key, "q_track": title, "q_artist": artist})
            resp_track = requests.get(f"{API}/matcher.track.get", params={"apikey": key, "q_track": title, "q_artist": artist})
            #gets json is a varaible
            song = resp_lyrics.json()
            track = resp_track.json()
            #gets returning json object
            artist_name = track['message']['body']['track']['artist_name']
            track_name = track['message']['body']['track']['track_name']
            lyrics = song["message"]["body"]["lyrics"]["lyrics_body"]
            resp = {'lyrics': lyrics, 'artist': artist, 'title': title, "track_name": track_name, "artist_name": artist_name}
            chart = get_chart_artists()
            username= Users.query.all()
            return render_template('home.html', resp=resp, form=form, chart=chart, username=username)
        #return render_template('home.html', track=track, artist=artist, title=title, form=form)
    else:
        chart = get_chart_artists()
        username= Users.query.all()
        return render_template('home.html', form=form, chart=chart, username=username)
        #resp_track = requests.get(f"{API}/matcher.lyrics.get", params={"apikey": key, "q_track": "", "q_artist": ""})
        #resp_artist = requests.get(f"{API}/artist.search", params={"apikey": key, "q_artist": ""})
        #return render_template('home.html', track=track, name=name, form=form)




@app.route('/favorites')
def fav_pg():

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    favs = Favorite.query.all()
    return render_template('favorites.html', favs=favs)


@app.route("/favorites/add", methods=["GET", "POST"])
def add_song():

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = AddFavSong()
    #fav = Favorite.query.get_or_404(favorite_id)

    if form.validate_on_submit():
        artist = form.artist.data
        title = form.title.data
        if artist and title:
            resp_track = requests.get(f"{API}/matcher.track.get", params={"apikey": key, "q_track": title, "q_artist": artist})

            track = resp_track.json()

            track_id = track['message']['body']['track']['track_id']
            artist_name = track['message']['body']['track']['artist_name']
            track_name = track['message']['body']['track']['track_name']

            new_song = Favorite(artist=artist_name, title=track_name, track_id=track_id)
            db.session.add(new_song)
            db.session.commit()

            userFavs = UserFavorites(user_id=g.user.id, favorite_id=Favorite.id)
            db.session.add(userFavs)
            db.session.commit()

        return redirect("/favorites")

    return render_template("addFav.html", form=form)




@app.route("/favorites/<int:favorite_id>", methods=["GET"])
def show_lyrics(favorite_id):

    if not g.user:
        flash("you do not have access to do this", 'danger')
        return redirect("/")

    fav = Favorite.query.get_or_404(favorite_id)
    
    resp_lyrics = requests.get(f"{API}/matcher.lyrics.get", params={"apikey": key, "q_track": fav.title, "q_artist": fav.artist})

    resp = resp_lyrics.json()

    lyrics = resp["message"]["body"]["lyrics"]["lyrics_body"]
        
    return render_template("favLyrics.html", lyrics=lyrics, fav=fav)
    
    
@app.route("/favorites/<int:favorite_id>/delete")
def fav_delete(favorite_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    fav = Favorite.query.get(favorite_id)
    #if fav.user_id != g.user.id:
        #flash("You are not authorized to do this", "danger")
        #return redirect("/")

    db.session.delete(fav)
    db.session.commit()
    return redirect("/favorites")






