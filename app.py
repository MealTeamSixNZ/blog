from flask import Flask, g, flash, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

# def get_db():
#     db=getattr(g,'_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#         db.row_factory = sqlite3.Row # this makes query results easier to work with
#     return db
    
# def init_db():
#     with app.app_context():
#         db = get_db()
#         with app.open_resource('schema.sql', mode='r') as f:
#             db.cursor().executescript(f.read())
#         db.commit()  

posts = [
     {'id':1, 'title':'First Post','content':'This is the content of the first post.'},
     {'id':2, 'title':'Second Post','content':'This is the content of the second post.'}
]
@app.route('/')
# def index():
#     db = get_db()
#     cur = db.execute('SELECT id, title, content FROM posts ORDER BY id DESC')
#     posts = cur.fetchall()
#     return render_template('index.html', posts=posts)

def index():
    return render_template('index.html', posts=posts)

postsCount = len(posts) + 1

@app.route('/create', methods=['GET','POST'])
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         if not title or not content:
#             flash('Title and content are required!')
#         else:
#             db = get_db()
#             db.execute('INSERT INTO posts (title, content) VALUES (?,?)',[title, content])
#             db.commit()
#             return redirect(url_for('index'))
#         return render_template('create.html')

def create():
    global postsCount
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title or not content:
            flash('Title and content is required!')
        else:
            postsCount += 1
            new_post = {'id':postsCount, 'title':title,'content':content}
            posts.append(new_post)
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
# def edit(post_id):
#     db = get_db()
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         db.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', [title, content, post_id])
#         db.commit()
#         return redirect(url_for('index'))
#     else:
#         post = db.execute('SELECT id, title, content FROM posts WHERE id = ?', [post_id]).fetchone()
#         return render_template('edit.html', post=post)

def edit(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)
    if post is None:
        return "Post not found", 404
    if request.method == 'POST':
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        return redirect(url_for('index'))
    return render_template('edit.html', post=post)

@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
# def delete(post_id):
#     db = get_db()
#     db.execute('DELETE FROM posts WHERE id = ?', [post_id])
#     db.commit()
#     return redirect(url_for('index'))

def delete(post_id):
    global posts
    print(post_id)
    posts = [post for post in posts if post['id'] != post_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
        # init_db()
        app.run(debug=True)
