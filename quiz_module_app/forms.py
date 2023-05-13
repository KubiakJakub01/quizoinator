from tkinter import Button
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, BooleanField,FieldList,Form,FormField
from wtforms.validators import DataRequired, Length

class QuizForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    num_questions = IntegerField('Number of Questions', validators=[DataRequired()])
    questions = FieldList(TextAreaField('Questions',validators=[DataRequired(),Length(max=4)]))
    answers = FieldList(TextAreaField('Answers',validators=[DataRequired(),Length(max=4)]))
    submit = SubmitField('Create Quiz')

class AnswerForm(Form):
    text = StringField('Answer', validators=[DataRequired(), Length(max=100)])
    is_correct = BooleanField('Correct?')
    submit = SubmitField('Add Answer Form')

class QuestionForm(FlaskForm):
    question_text = TextAreaField('Question', validators=[DataRequired(), Length(max=500)])
    answers = FieldList(FormField(AnswerForm),min_entries=1,max_entries=4)
    submit = SubmitField('Add QuestionForm')

class QuizView(Form):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    #solve = Button('Create Quiz')


