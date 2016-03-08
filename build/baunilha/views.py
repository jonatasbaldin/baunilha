from baunilha import app
from baunilha.twitter_logic import BaunilhaTwitter
from flask import render_template, redirect, url_for, session
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


def twitter_auth():
    """
    Globally authenticate Twitter.
    """
    global twitter
    twitter = BaunilhaTwitter()
    twitter.Connect(consumer_key=app.config['TWITTER_CONSUMER_KEY'],
                    consumer_secret=app.config['TWITTER_CONSUMER_SECRET'],
                    access_token_key=app.config['TWITTER_ACCESS_TOKEN_KEY'],
                    access_token_secret=app.config['TWITTER_ACCESS_TOKEN_SECRET'])


class FormGetUser(Form):
    """
    Form to get Twitter user to retrive its tweets.
    Parameters:
    user: username as string
    submit: submit button
    """
    user = StringField(validators=[DataRequired()])
    submit_ptbr = SubmitField(label='Leia pra mim!')
    submit_en = SubmitField(label='Read to me!')


def validate_form_getuser(form):
    """
    Validate FormGetUser, provided to eliminate duplicated code.
    Parameters:
    form: form to Validate, in this case, an instance of FormGetUser
    """
    if form.validate_on_submit():
        user = form.user.data
        form.user.data = ''
        if form.submit_en.data:
            session['lang'] = 'en'
        elif form.submit_ptbr.data:
            session['lang'] = 'ptbr'
        return {'user': user, 'lang': session['lang']}


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Generates index page.
    """

    form = FormGetUser()
    valid_form = validate_form_getuser(form)
    if valid_form:
        return redirect(url_for('user', user=valid_form['user'], lang=valid_form['lang']))

    return render_template('index.html', form=form)


@app.route('/<user>/', methods=['GET', 'POST'])
def user(user):
    """
    Gerenates a page with users' tweets.
    """

    # if the form is not used (direct GET do /<user>)
    # we add a default language
    if 'lang' not in session:
        session['lang'] = 'ptbr'

    # performs authentication
    twitter_auth()

    form = FormGetUser()
    valid_form = validate_form_getuser(form)
    if valid_form:
        return redirect(url_for('user', user=valid_form['user'], lang=valid_form['lang']))

    tweets = twitter.GetTweets(user)

    if tweets['error']:
        return render_template('index.html',
                               error=tweets['error'],
                               message=tweets['message'],
                               form=form)

    return render_template('user.html',
                           tweets=tweets['tweets'],
                           user=tweets['user'],
                           user_img=tweets['user_img'],
                           lang=session['lang'],
                           form=form)


@app.route('/<user>/status/<id>')
def status(user, id):
    """
    Generates a page with a single tweet, using tweet's status.
    """

    # if the form is not used (direct GET do /<user>)
    # we add a default language
    if 'lang' not in session:
        session['lang'] = 'ptbr'

    # performs authentication
    twitter_auth()

    form = FormGetUser()
    valid_form = validate_form_getuser(form)
    if valid_form:
        return redirect(url_for('user', user=valid_form['user'], lang=valid_form['lang']))

    tweet = twitter.GetSingleTweet(user, id)

    if tweet['error']:
        return render_template('index.html',
                               error=tweet['error'],
                               message=tweet['message'],
                               form=tweet)

    return render_template('user.html',
                           single_tweet=tweet['single_tweet'],
                           single_tweet_id=tweet['single_tweet_id'],
                           user_img=tweet['user_img'],
                           user=tweet['user'],
                           lang=session['lang'],
                           form=form)


@app.errorhandler(404)
def page_not_found(e):
    """ Handles HTTP 404 """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """ Handles HTTP 500 """
    return render_template('500.html'), 500
