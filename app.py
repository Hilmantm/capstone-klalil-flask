import json

import pandas as pd
from flask import Flask, request

from hybridization import recommendation_place
from knowledge_constraint import knowledge_data

app = Flask(__name__)


# Route index
@app.route('/')
def index():
    return 'Hallo, selamat datang di Website saya!!!!'

@app.route('/recomendation')
def place_recommendation():
    recommendation = recommendation_place()
    return dict({
        "success": True,
        "data": recommendation.to_dict(orient='records')
    })

# Route statis
@app.route('/setting')
def show_setting():
    return 'Anda berada pada halaman setting'


# Route dinamis
@app.route('/profile/<username>')
def show_profile(username):
    return 'Anda berada pada halaman profile %s' % username


# Route dinamis + spesifik tipe data yang diterima
@app.route('/blog/<int:blog_id>')
def show_blog(blog_id):
    return 'Anda berada pada halaman blog dengan id %d' % blog_id


# Route post
@app.route('/profile/<username>', methods=['POST'])
def post_data(username):
    if request.method == 'POST':
        return 'Email dari ' + username + ' adalah ' + request.form['email']


if __name__ == '__main__':
   app.run(debug = True)