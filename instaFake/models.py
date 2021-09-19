import os
from TikTokApi import TikTokApi
from flask import Flask, render_template, request, flash, redirect, session, g, abort
import requests
from newsapi import NewsApiClient
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import os
from forms import LoginForm, SignupForm, UserEditForm, CommentForm, NewPost, FeedQuery
from models import db, connect_db, User, Follows, Likes, Posts

newsapi = NewsApiClient(api_key='b4181a4ffbd44b9cb5d1441b94c80ee2')
CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pictagram'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

    

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

def hashtag_recents():
    """gets the most recent post and vids"""



#home page route#######################################################
#verifyFp = "verify_kt6pvkl0_jcZ7KsSS_jLb1_43QO_B46v_Ab08OxBzymTB"
api = TikTokApi.get_instance()
results = 20
trending = api.by_trending(count=results, custom_verifyFp="verify_kt6pvkl0_jcZ7KsSS_jLb1_43QO_B46v_Ab08OxBzymTB")

#print(hashtag)

@app.route('/feed', methods=["POST", "GET"])
def hashtag():
    """shows feed of hashtags"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    #resp = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=b4181a4ffbd44b9cb5d1441b94c80ee2')
    headlines = newsapi.get_top_headlines()
    articles = headlines["articles"]

    desc= []
    news = []
    img = []
    url = []

    for res in range(len(articles)):
        my_articles = articles[res]
        news.append(my_articles['title'])
        desc.append(my_articles['description'])
        img.append(my_articles['urlToImage'])
        url.append(my_articles['url'])

        art_list = zip(news, desc, img, url)
    return render_template('feed.html', resp=art_list)

        

@app.route('/')
def homepage():

    if g.user:
        following_ids = [f.id for f in g.user.following] + [g.user.id]

        posts = (Posts
                    .query
                    .filter(Posts.user_id.in_(following_ids))
                    .order_by(Posts.timestamp.desc())
                    .limit(100)
                    .all())
        # Prints the id of the tiktok

        liked_msg_ids = [msg.id for msg in g.user.likes]

        return render_template('home.html', posts=posts, likes=liked_msg_ids, api=trending)

    else:
        return render_template('home-anon.html')

#login/logout and signup############################################
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = SignupForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data,
                profile_img=form.profile_img.data or User.profile_img.default.arg
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('/users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.email.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have logged out.", 'success')
    return redirect("/login")
#################################################################


#Users app routes################################################

@app.route('/users')
def list_users():
    """Page with listing of users.
    Can take a 'q' param in querystring to search by that username.
    """

    search = request.args.get('q')

    posts = (Posts
                .query
                .filter(Posts.user_id == g.user.id)
                .order_by(Posts.timestamp.desc())
                .limit(100)
                .all())

    if not search:
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

    return render_template('users/index.html', posts=posts, users=users)


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get(user_id)
    # snagging messages in order from the database;
    # user.messages won't be in order by default
    posts = (Posts
                .query
                .filter(Posts.user_id == user_id)
                .order_by(Posts.timestamp.desc())
                .limit(100)
                .all())
    likes = [post.id for post in user.likes]
    return render_template('posts/show.html', user=user, posts=posts, likes=likes)


@app.route('/users/<int:user_id>/following')
def show_following(user_id):
    """Show list of people this user is following."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    return render_template('users/following.html', user=user)


@app.route('/users/<int:user_id>/followers')
def users_followers(user_id):
    """Show list of followers of this user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    return render_template('users/followers.html', user=user)


@app.route('/users/follow/<int:follow_id>', methods=['POST'])
def add_follow(follow_id):
    """Add a follow for the currently-logged-in user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    followed_user = User.query.get_or_404(follow_id)
    g.user.following.append(followed_user)
    db.session.commit()

    return redirect(f"/users/{g.user.id}/following")


@app.route('/users/stop-following/<int:follow_id>', methods=['POST'])
def stop_following(follow_id):
    """Have currently-logged-in-user stop following this user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    followed_user = User.query.get(follow_id)
    g.user.following.remove(followed_user)
    db.session.commit()

    return redirect(f"/users/{g.user.id}/following")

@app.route('/users/<int:user_id>/likes', methods=["GET"])
def show_likes(user_id):
    if not g.user:
        flash("you do not have access to this.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    return render_template('users/likes.html', user=user, likes=user.likes)


@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""
    # IMPLEMENT THIS
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.profile_img = form.profile_img.data or "/static/images/warbler-hero.jpg"
        user.bio = form.bio.data
        user.location = form.location.data

        db.session.commit()
        return redirect(f"/users/{user.id}")

    return render_template('users/edit.html', form=form, user_id=user.id)

@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")

###############################################################################


#Posts######################################################################

@app.route('/posts/new', methods=["GET", "POST"])
def posts_add():
    """Add a message:
    Show form if GET. If valid, update message and redirect to user page.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = NewPost()

    if form.validate_on_submit():
        post = Posts(text=form.text.data,
                     image_url=form.image_url.data)
        g.user.post.append(post)
        db.session.commit()

        return redirect(f"/users/{g.user.id}")

    return render_template('posts/newPost.html', form=form)


@app.route('/posts/<int:post_id>', methods=["GET"])
def posts_show(post_id):
    """Show a message."""

    msg = Posts.query.get_or_404(post_id)
    return render_template('posts/show.html', message=msg)


@app.route('/posts/<int:message_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Delete a message."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    msg = Posts.query.get(post_id)
    if msg.user_id != g.user.id:
        flash("you do not have access to do this.", "danger")
        return redirect("/")

    db.session.delete(msg)
    db.session.commit()

    return redirect(f"/users/{g.user.id}")


@app.route('/posts/<int:message_id>/like', methods=['POST'])
def add_like(post_id):
    """like warbles by logged in user"""

    if not g.user:
        flash("you do not have access to do this", 'danger')
        return redirect("/")

    liked_message = Posts.query.get_or_404(post_id)
    if liked_message.user_id == g.user.id:
        return abort(403)

    user_likes = g.user.likes

    if liked_message in user_likes:
        g.user.likes = [like for like in user_likes if like != liked_message]
    else:
        g.user.likes.append(liked_message)

    db.session.commit()
    return redirect("/")

################# hashtag search feed




