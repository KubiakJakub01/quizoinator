"""
Module for relationship utils
"""
from flask import flash, redirect, url_for, render_template
from src.models import relationship_status

class RelationshipUtils:
    """
    Class for relationship utils
    """

    def __init__(self, db, Users, Relationship):
        self.db = db
        self.Users = Users
        self.Relationship = Relationship

    def add_relationship(self, id, current_user_id):
        """
        Add relationship
        """
        user = self.Users.query.filter_by(_id=id).first()
        if user:
            if user._id == current_user_id:
                flash("You can't add yourself!", "error")
                return redirect(url_for("users.user_home"))
            if self.Relationship.query.filter_by(
                user_a_id=current_user_id, user_b_id=user._id
            ).first():
                flash("You are already friends!", "error")
                return redirect(url_for("users.user_home"))
            if self.Relationship.query.filter_by(
                user_a_id=user._id, user_b_id=current_user_id
            ).first():
                flash("You are already friends!", "error")
                return redirect(url_for("users.user_home"))
            new_relationship = self.Relationship(
                user_a_id=current_user_id,
                user_b_id=user._id,
                status=relationship_status["pending"],
            )
            self.db.session.add(new_relationship)
            self.db.session.commit()
            flash("Friend request sent!", "info")
            return redirect(url_for("users.user_home"))
        flash("User not found!", "error")
        return redirect(url_for("users.user_home"))

    def accept_relationship(self, id):
        """
        Accept relationship
        """
        relationship = self.Relationship.query.filter_by(
            _id=id
        ).first()
        if relationship:
            if relationship.status == relationship_status["pending"]:
                relationship.status = relationship_status["accepted"]
                self.db.session.commit()
                flash("Friend request accepted!", "info")
                return redirect(url_for("users.user_home"))
            flash("Friend request already accepted!", "error")
            return redirect(url_for("users.user_home"))
        flash("Friend request not found!", "error")
        return redirect(url_for("users.user_home"))

    def reject_relationship(self, id):
        """
        Reject
        """
        relationship = self.Relationship.query.filter_by(
            _id=id
        ).first()
        if relationship:
            if relationship.status == relationship_status["pending"]:
                self.db.session.delete(relationship)
                self.db.session.commit()
                flash("Friend request rejected!", "info")
                return redirect(url_for("users.user_home"))
            flash("Friend request already accepted!", "error")
            return redirect(url_for("users.user_home"))
        flash("Friend request not found!", "error")
        return redirect(url_for("users.user_home"))

    def get_relationships(self, id):
        """
        Get relationships
        """
        # Get all relationships where user_a_id or user_b_id is id
        relationships = self.Relationship.query.filter(
            (self.Relationship.user_a_id == id)
            | (self.Relationship.user_b_id == id)
        ).all()
        return relationships
    
    def friends(self, id):
        """
        Get friends
        """
        friends = self.get_relationships(id)
        print(friends)
        return render_template("friends.html", friends=friends)
