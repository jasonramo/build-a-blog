from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:admin@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True  #provides the sql commands in the terminal
db = SQLAlchemy(app)
app.secret_key = 'mB4kPa934nwmi2o'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(240))
    #owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        #self.owner = owner

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        post_title_name = request.form['title']
        post_body_name = request.form['body']
        if post_title_name == "" or post_body_name == "":
            flash("You've left a mandatory field blank. Please fill in both fields to post your entry", 'error')
        else:    
            new_post = Blog(post_title_name, post_body_name)

            db.session.add(new_post)
            db.session.commit()
            return redirect('/blogs')

    return render_template('newpost.html',title="Build A Blog")


@app.route('/blogs', methods=['POST', 'GET'])
def blogs():

    posts = Blog.query.all()

    return render_template('blogs.html', title='Build A Blog', posts=posts)

if __name__ == '__main__':            
    app.run()