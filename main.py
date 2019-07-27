from flask import Flask, request, redirect, render_template,flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:building@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body

posts = []

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    post_id = request.args.get('id')
    title = "Build a Blog"

    if post_id:
        blog = Blog.query.filter_by(id = post_id).all()
        # title = blog.title
        return render_template('blog.html', title = title, blog = blog, post_id = post_id)
    else:
        blog = Blog.query.order_by(Blog.id.desc()).all()
        return render_template('index.html', title = title, blog = blog)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-entry']
        title_error = ''
        body_error = ''

        if not blog_title:
            title_error = "Please enter a blog title"
        if not blog_body:
            body_error = "Please enter a blog entry"

        if not body_error and not title_error:
            new_entry = Blog(blog_title, blog_body)
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/blog?id={}'.format(new_entry.id))
        else:
            return render_template('newpost.html', title='New Entry', title_error=title_error, body_error=body_error,
                                   blog_title=blog_title, blog_body=blog_body)

    return render_template('newpost.html', title='New Entry')

if  __name__ == "__main__":
    app.run()
