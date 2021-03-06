# app.py


from flask import Flask
from flask import request, render_template,Response
from flask.ext.sqlalchemy import SQLAlchemy
from config import BaseConfig


app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)


from models import *


@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hello World!"

@app.route('/env', methods=['GET'])
def printenv():
    rval = """
Headers
---
{headers}
    """.format(headers=request.headers)
    resp = Response(rval)
    resp.headers['Content-Type'] = 'text/plain'
    return resp


@app.route('/bpost', methods=['GET', 'POST'])
def bpost():
    if request.method == 'POST':
        text = request.form['text']
        post = Post(text)
        db.session.add(post)
        db.session.commit()
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)



if __name__ == '__main__':
    app.run()
