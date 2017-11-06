# -*- coding: utf-8 -*-

__author__ = 'cipajozef@gmail.com'

import werkzeug.exceptions as ex
from flask import Flask, jsonify, request, render_template, redirect
import configparser
import redis
import random
import string
from slugify import slugify
import unidecode
import validators

# Config
config = configparser.ConfigParser()
config.read('config.ini')

# Redis setup
redis_config = config['REDIS']
redis = redis.StrictRedis(host=redis_config['host'], port=redis_config['port'], db=0)

# App setup
config = config['DEFAULT']
app = Flask(__name__, static_folder='public')
msg = ''

# Index page, entry point
@app.route('/', methods=['GET'])
def index():
    global msg

    error_msg = ''
    if msg: 
        error_msg = msg
        msg = '' # Reset message

    return render_template('index.html', msg=error_msg)

# Handling add request
@app.route('/add-url', methods=['POST'])
def add_url():

    # Check if URL has been given
    url = request.form.get('url')
    if not url:
        return jsonify({'msg': 'You have to enter URL'})

    # Check if given string is valid URL
    if not validators.url(url):
        return jsonify({'msg': 'Don\'t try to fuck with me, I know it\'s not a valid URL'})

    # Key for given url
    url_key = redis_config['prefix']
    name = request.form.get('name')

    # Check if name is not empty
    if name:
        # Check if given name already exists in redis
        if redis.exists(url_key + name + config['customKeyNamePrefix']):
            return jsonify({'msg': 'This name is already in use. Try something else.'})

        # Make slug from name
        name = unidecode.unidecode(slugify(name))

        # Assign custom name with prefix to avoid showing this url for other users who enter same url
        redis.set(url_key + name + config['customKeyNamePrefix'], url)
    else:

        # If this is set to True, it will check if given url isn't already saved, if it is, just return key
        if config['sameKeyForSameUrl']:

            # Check if given url has been already saved
            for key in redis.keys(redis_config['prefix'] + "*"):
                if (redis.get(key).decode('utf-8') == url and config['customKeyNamePrefix'] not in key.decode('utf-8')):

                    # Remove from key redis prefix and custom name prefix if exists
                    name = key.decode('utf-8').replace(redis_config['prefix'], '').replace(config['customKeyNamePrefix'], '')
        
        if not name:
            # Generate random key
            name = ''.join(random.choice(string.digits + string.ascii_lowercase + string.ascii_uppercase) for _ in range(int(config['nameLength'])))

            # Save to Redis
            redis.set(url_key + name, url)

    # Return response
    return jsonify({
        'yourUrl': config['baseUrl'] + '/' + name
    })

# Redirecting to full saved URL
@app.route('/<key>', methods=['GET'])
def return_link(key):

    global msg

    # Try to find url by key
    url = redis.get(redis_config['prefix'] + key)

    # Try to find url by custom name key
    custom_key_url = redis.get(redis_config['prefix'] + key + config['customKeyNamePrefix'])

    if url:
        return redirect(url.decode('utf-8'))
    elif custom_key_url:
        return redirect(custom_key_url.decode('utf-8'))
    else:
        # Redirect to index with message
        msg = 'Url "<i>{0}</i>" doesn\'t exist'.format(config['baseUrl'] + '/' + key)
        return redirect('') 

if __name__ == "__main__":
    app.run(debug=config['debug'])