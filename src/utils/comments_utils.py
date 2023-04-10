"""Module with comments utilities"""
from flask import render_template, redirect, url_for, flash


class CommentsUtils:
    """Comments utils"""

    def __init__(self, db, Comments):
        self.db = db
        self.Comments = Comments

    def get_comments_from_post(self, post_id):
        """Get comments from post"""
        comments = self.Comments.query.filter_by(post_id=post_id).all()
        return comments

    def add_comment(self, id, form, author_id):
        """Add comment to db"""
        if form.validate_on_submit():
            comment = self.Comments(
                post_id=id,
                author_id=author_id,
                comment=form.comment.data,
            )
            self.db.session.add(comment)
            self.db.session.commit()
            flash("Comment added!", "success")
            return redirect(url_for("blog.view_post", id=id))
        return redirect(url_for("blog.view_post", id=id))

    def update_comment(self, id, form, author_id):
        """Update comment in db"""
        if author_id != self.Comments.query.filter_by(_id=id).first().author_id:
            flash("You can't update this comment!", "error")
            return redirect(url_for("blog.view_posts"))
        comment = self.Comments.query.filter_by(_id=id).first()
        if form.validate_on_submit():
            comment.content = form.content.data
            self.db.session.commit()
            flash("Comment updated!", "success")
            return redirect(url_for("blog.view_post", id=comment.post_id))
        form.content.data = comment.content
        return render_template("update.html", form=form)

    def delete_comment(self, id, author_id):
        """Delete comment from db"""
        if author_id != self.Comments.query.filter_by(_id=id).first().author_id:
            flash("You can't delete this comment!", "error")
            return redirect(url_for("blog.view_posts"))
        comment = self.Comments.query.filter_by(_id=id).first()
        self.db.session.delete(comment)
        self.db.session.commit()
        flash("Comment deleted!", "success")
        return redirect(url_for("blog.view_post", id=comment.post_id))
