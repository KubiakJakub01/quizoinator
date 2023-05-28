from .extensions import db


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    #num_questions = db.Column(db.Integer)
    questions = db.relationship('Question', backref='quiz', lazy=True)

    def __repr__(self):
        return f"Quiz('{self.title}', '{self.description}')"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    answers = db.relationship('Answer', backref='question', lazy=True)

    def __repr__(self):
        return f"Question('{self.text}')"


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    def __repr__(self):
        return f"Answer('{self.text}', {self.is_correct})"
