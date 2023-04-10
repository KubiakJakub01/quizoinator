"""
Module for posts utils
"""
from pathlib import Path
from flask import render_template, flash, redirect, url_for


class PostsUtils:
    """Posts utils"""

    def __init__(self, db, Posts, PostsLikes, blog_dir):
        self.db = db
        self.Posts = Posts
        self.PostsLikes = PostsLikes
        self.blog_dir = Path(blog_dir)

    def view_posts(self):
        """View posts"""
        posts = self.Posts.query.order_by(self.Posts.data_created.desc()).all()
        return render_template(str(self.blog_dir / "posts.html"), posts=posts)

    def view_post(self, id):
        """View post"""
        post = self.Posts.query.get_or_404(id)
        return render_template(str(self.blog_dir / "post.html"), 
                               post=post)

    def update_post(self, id, form, author_id):
        """Update post"""
        post_to_update = self.Posts.query.get_or_404(id)
        if post_to_update.author_id != author_id:
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
            return render_template(
                str(self.blog_dir / "update_post.html"), form=form, post=post_to_update
            )

    def delete_post(self, id, author_id):
        """Delete post"""
        post_to_delete = self.Posts.query.get_or_404(id)
        if post_to_delete.author_id != author_id:
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

    def add_post(self, form, author_id):
        """Add post"""
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            post = self.Posts(title=title, content=content, author_id=author_id)
            form.title.data = ""
            form.content.data = ""
            self.db.session.add(post)
            self.db.session.commit()
            flash("Post created!", "info")
            return redirect(url_for("view_posts"))
        else:
            return render_template(str(self.blog_dir / "add_post.html"), form=form)

    def search_post(self, form):
        """Search post"""
        if form.validate_on_submit():
            search = form.searched.data
            posts = self.Posts.query.filter(
                self.Posts.content.like("%" + search + "%")
            ).all()
            return render_template(
                str(self.blog_dir / "search_post.html"), posts=posts, search=search
            )
        else:
            return redirect(url_for("view_posts"))

    def like_post(self, id, author_id):
        """Like post"""
        post = self.Posts.query.get_or_404(id)
        if post.author_id == author_id:
            flash("You can't like your own post!", "error")
            return redirect(url_for("view_posts"))
        post_like = self.PostsLikes.query.filter_by(
            post_id=id, author_id=author_id
        ).first()
        if post_like:
            flash("You already liked this post!", "error")
            return redirect(url_for("view_posts"))
        post_like = self.PostsLikes(post_id=id, author_id=author_id)
        self.db.session.add(post_like)
        self.db.session.commit()
        flash("Post liked!", "info")
        return redirect(url_for("view_posts"))
