# -*- coding: utf-8 -*-
import os
from Utils import Utils
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index_ja():
    """
    Japanese page

    return:
        first argument: Template file
        second argument: Link a button to this URL with <a> tag.
        third argument: The information of this site
        forth argument: Language code as subdirectory
    """
    api.set_description(u'インスタグラムでの片思いや相互フォローをチェックできるアプリ InstaChecker')
    api.set_short_description(u'インスタグラムのフォローチェックが簡単に。')
    return render_template('index_ja.html', url=url, info=api.basic_information, lang='')

@app.route('/id')
def index_id():
    """
    Indonesian Page
    """
    basic_information['description'] = 'cara yang untuk melihat siapa yang tidak memfollow kamu atau yang unfollowers kamu'
    basic_information['short_description'] = 'cara yang untuk melihat siapa yang tidak memfollow kamu atau yang unfollowers kamu'
    return render_template('index_id.html', url=url, info=api.basic_information, lang='/id')

@app.route('/result')
def result():
    # Set code getting from query of redirected URL
    api.set_code(request.args.get('code'))

    # Set access token
    api.request_access_token()

    # Get your follows and followers
    follows = api.get_follows()
    followers = api.get_followers()

    # Get the list of accounts you follow and be followed by.
    friends = api.get_list_of_friends(follows, followers)
    # Get the list of accounts you follow but not be followed by.
    follows_only = api.get_list_of_follows(friends, follows)
    # Get the list of accounts you don't follow but be followed by.
    followed_only = api.get_list_of_followers(friends, followers)

    length = {}

    length['friends'] = len(friends)
    length['follows_only'] = len(follows_only)
    length['followed_only'] = len(followed_only)

    return render_template(
        'result.html',
        info=api.basic_information,
        length=length,
        friends=friends,
        follows_only=follows_only,
        followed_only=followed_only
    )

@app.route('/fin')
def end():
    exit()

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', info=basic_information)

@app.route('/contact')
def contact():
    return render_template('contact.html', info=basic_information)


if __name__ == '__main__':
    api = Utils()

    # Set website name and URL
    api.set_url('http://localhost:5000')
    # api.set_name('InstaChecker')
    api.set_name('InstaChecker')

    # If you use this, set environment variables
    api.set_client_id(os.environ['client_id'])
    api.set_client_secret(os.environ['client_secret'])

    # Set a valid redirect URL.
    # If you change this, you have to see the setting in instagram developer page.
    api.redirect_url = api.basic_information['url'] + '/result'
    url = api.make_url()

    app.run()
