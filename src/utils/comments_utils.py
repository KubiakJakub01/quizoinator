"""Module with comments utilities"""
from pathlib import Path
from flask import render_template, redirect, url_for, flash
from flask_login import current_user


class CommentsUtils:
    """Comments utils"""

    def __init__(self, db, Comments, comments_dir):
        self.db = db
        self.Comments = Comments
        self.comments_dir = Path(comments_dir)

    def get_comments_from_post(self, post_id):
        """Get comments from post"""
        comments = self.Comments.query.filter_by(post_id=post_id).all()
        return comments

    def add_comment(self, id, form):
        """Add comment to db"""
        if form.validate_on_submit():
            comment = self.Comments(
                post_id=id,
                author_id=current_user._id,
                comment=form.comment.data,
            )
            self.db.session.add(comment)
            self.db.session.commit()
            flash("Comment added!", "success")
            return redirect(url_for("view_post", id=id))
        return redirect(url_for("view_post", id=id))

    def update_comment(self, id, form):
        """Update comment in db"""
        if current_user._id != self.Comments.query.filter_by(_id=id).first().author_id:
            flash("You can't update this comment!", "error")
            return redirect(url_for("view_posts"))
        comment = self.Comments.query.filter_by(_id=id).first()
        if form.validate_on_submit():
            comment.content = form.content.data
            self.db.session.commit()
            flash("Comment updated!", "success")
            return redirect(url_for("view_post", id=comment.post_id))
        form.content.data = comment.content
        return render_template(str(self.comments_dir / "update.html"), form=form)

    def delete_comment(self, id):
        """Delete comment from db"""
        if current_user._id != self.Comments.query.filter_by(_id=id).first().author_id:
            flash("You can't delete this comment!", "error")
            return redirect(url_for("view_posts"))
        comment = self.Comments.query.filter_by(_id=id).first()
        self.db.session.delete(comment)
        self.db.session.commit()
        flash("Comment deleted!", "success")
        return redirect(url_for("view_post", id=comment.post_id))
