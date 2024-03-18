from flask import Flask, flash, render_template, request, redirect, url_for

app = Flask(__name__)
posts = [
     {'id':1, 'title':'First Post','content':'This is the content of the first post.'},
     {'id':2, 'title':'Second Post','content':'This is the content of the first post.'}
]
@app.route('/')
def index():
    return render_template('index.html', posts=posts)
@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title or not content:
            flash('Title and content is required!')
        else:
            new_id = len(posts) + 1
            new_post = {'id':new_id, 'title':title,'content':content}
            posts.append(new_post)
            return redirect(url_for('index'))
    return render_template('create.html')
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
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
def delete(post_id):
    global posts
    posts = [post for post in posts if post['id'] != post_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
        app.run(debug=True)
