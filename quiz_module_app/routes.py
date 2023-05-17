from flask import Blueprint, render_template, flash, redirect, url_for, request, flash, json, session
from sqlalchemy import MetaData

from .extensions import db
from .models import Question, Quiz, Answer
from .forms import QuizForm, QuestionForm, AnswerForm


main = Blueprint('main', __name__)


@main.route("/add/quiz/json", methods=['POST'])
def add_quiz_json():
    response_arr = json.loads(request.data)
    quiz_title_desc = response_arr[0]
    questions_arr = response_arr[1]
    answers_arr = response_arr[2]
    titleFromJson = quiz_title_desc.get('title')
    descriptionFromJson = quiz_title_desc.get('description')
    print(titleFromJson," ",descriptionFromJson)
    new_quiz = Quiz(title=titleFromJson, description=descriptionFromJson)
    try:
        db.session.add(new_quiz)
        db.session.commit()
    except:
        return 'Nie udało sie zapisac quizu!'

    for question_object in questions_arr:
        new_question = Question(text=question_object.get(
        'question_text'), quiz_id=new_quiz.id)
        try:
            db.session.add(new_question)
            db.session.commit()
        except:
            return 'Nie udało sie zapisac pytania!'
        print("question_object: ",question_object)
        for answer_object in answers_arr:
            tempIsCorrect = False
            print("answer_object: ",answer_object)
            if (answer_object.get('answerToQuestion') == question_object.get('id')):
                if (answer_object.get('is_correct') == "1"):
                    tempIsCorrect = True
                new_answer = Answer(text=answer_object.get('answer_text'), is_correct=tempIsCorrect, 
                                        question_id=new_question.id)
                try:
                    db.session.add(new_answer)
                    db.session.commit()
                except:
                    return 'Nie udało sie zapisac odpowiedzi!'

    return redirect('/')


@main.route('/solve/quiz/<int:quiz_id_parameter>', methods=['POST', 'GET'])
def solve_quiz(quiz_id_parameter):
    quiz = Quiz.query.filter_by(id=quiz_id_parameter).first()
    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    score = 0
    if request.method == 'POST':
        correct_answers = []
        user_answers = []
        for question in questions:
            answers = Answer.query.filter_by(question_id=question.id).all()
            print("answers: ",answers)
            for answer in answers:
                if answer.is_correct is True:
                    correct_answers.append(answer.id)
            print('correct_answers: ', correct_answers)
            print('request.form.getlist(question.id): ',
                  request.form.getlist(str(question.id)))
            for user_answer in request.form.getlist(str(question.id)):
                user_answers.append(int(user_answer))
        print('user_answers: ',user_answers)
        incorrect_user_answers = 0
        if len(user_answer) > len(correct_answers):
            incorrect_user_answers = len(user_answer) - len(correct_answers)
        score = score + len(list(set(correct_answers).intersection(user_answers))) - incorrect_user_answers
        return render_template('display_score.html', score=score)
    else:
        return render_template('solve_quiz.html', quiz=quiz, questions=questions)


@main.route('/add/answer/<int:question_id_parameter>', methods=['POST', 'GET'])
def add_answer(question_id_parameter):
    question = Question.query.filter_by(id=question_id_parameter).first()
    if request.method == 'POST':
        is_answer_correct = False
        if request.form.get('answer_chk'):
            is_answer_correct = True
        new_answer = Answer(
            text=request.form['answer_text'], is_correct=is_answer_correct, question_id=question.id)
        try:
            db.session.add(new_answer)
            db.session.commit()
            return redirect(url_for('main.edit_quiz', quiz_id_parameter=question.quiz_id))
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('add_answer.html', question=question)


@main.route('/delete/quiz/<int:quiz_id_parameter>')
def delete_quiz(quiz_id_parameter):
    quiz_to_delete = Quiz.query.get_or_404(quiz_id_parameter)
    try:
        db.session.delete(quiz_to_delete)
        db.session.commit()
        flash(f"Deleted quiz with id: {quiz_id_parameter}")
        return redirect('/')
    except:
        return 'There was an issue deleting quiz'


@main.route('/edit/quiz/<int:quiz_id_parameter>', methods=['POST', 'GET'])
def edit_quiz(quiz_id_parameter):
    quiz = Quiz.query.filter_by(id=quiz_id_parameter).first()
    if request.method == 'POST':
        new_question = Question(
            text=request.form['question_text'], quiz_id=quiz.id)
        print(request.form['question_text'])
        try:
            db.session.add(new_question)
            db.session.commit()
            return redirect(url_for('main.edit_quiz', quiz_id_parameter=quiz.id))
        except:
            return 'There was an issue adding your task'

    else:
        questions = Question.query.filter_by(quiz_id=quiz.id).all()
        return render_template('edit_quiz.html', questions=questions, quiz=quiz)


@main.route('/', methods=['GET','POST'])
def index():
    
    if request.method == 'POST':
       searched_quiz = request.form['searchQuiz']
       quizes = Quiz.query.filter(Quiz.title.ilike(f'%{searched_quiz}%')).all()
       return render_template('index.html', quizes=quizes)
    else:
        quizes = Quiz.query.all()
        return render_template('index.html', quizes=quizes)


@main.route('/quiz/create/', methods=['GET'])
def quiz_create():
    quizForm = QuizForm()
    return render_template('quiz_create.html', form=quizForm)
