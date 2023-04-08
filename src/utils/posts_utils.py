"""
Module for posts utils
"""
from flask import render_template, flash, redirect, url_for


class PostsUtils:
    """Posts utils"""

    def __init__(self, db, Posts):
        self.db = db
        self.Posts = Posts

    def view_posts(self):
        """View posts"""
        posts = self.Posts.query.order_by(self.Posts.data_created.desc()).all()
        return render_template("posts.html", posts=posts)

    def view_post(self, id):
        """View post"""
        post = self.Posts.query.get_or_404(id)
        return render_template("post.html", post=post)

    def update_post(self, id, form, current_user):
        """Update post"""
        post_to_update = self.Posts.query.get_or_404(id)
        if post_to_update.author != current_user:
            flash("You can't update this post!", "error")
            return redirect(url_for("view_posts"))
        if form.validate_on_submit():
            post_to_update.title = form.title.data
            post_to_update.content = form.content.data
            form.title.data = ""
            form.content.data = ""
            self.db.session.commit()
            flash("Post updated!", "info")
            return redirect(url_for("view_posts"))
        else:
            form.title.data = post_to_update.title
            form.content.data = post_to_update.content
            return render_template("update_post.html", form=form, post=post_to_update)

    def delete_post(self, id):
        """Delete post"""
        post_to_delete = self.Posts.query.get_or_404(id)
        if post_to_delete.author != self.current_user:
            flash("You can't delete this post!", "error")
            return redirect(url_for("view_posts"))
        try:
            self.db.session.delete(post_to_delete)
            self.db.session.commit()
            flash("Post deleted!", "info")
            return redirect(url_for("view_posts"))
        except:
            flash("There was an issue deleting your post", "error")
            return redirect(url_for("view_posts"))

    def add_post(self, form, author):
        """Add post"""
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            author = author
            post = self.Posts(title=title, content=content, author=author)
            form.title.data = ""
            form.content.data = ""
            self.db.session.add(post)
            self.db.session.commit()
            flash("Post created!", "info")
            return redirect(url_for("view_posts"))
        else:
            return render_template("add_post.html", form=form)
