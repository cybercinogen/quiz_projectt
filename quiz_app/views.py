# quiz_app/views.py

import random
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Question, QuizSession

def home(request):
    # Let user pick number of questions
    # We'll have a form in home.html to select question_limit.
    return render(request, 'quiz_app/home.html')

def start_quiz(request):
    length = request.GET.get('length', 10)  # get chosen length from form (default 10)
    new_session = QuizSession.objects.create(question_limit=int(length))
    new_session.start_time = timezone.now()
    new_session.save()
    request.session['quiz_session_id'] = str(new_session.session_id)
    return redirect('get_question')

def get_question(request):
    session_id = request.session.get('quiz_session_id', None)
    if not session_id:
        return redirect('home')

    quiz_session = QuizSession.objects.get(session_id=session_id)
    seen = quiz_session.get_seen_questions()

    all_questions = Question.objects.all()
    if not all_questions.exists():
        return redirect('quiz_result')

    # Filter out seen questions
    unseen_questions = all_questions.exclude(id__in=seen)

    # If no unseen questions remain, reset and allow repetition
    if not unseen_questions.exists():
        quiz_session.reset_seen_questions()
        unseen_questions = all_questions

    question = unseen_questions.order_by('?').first()  # random unseen question
    context = {'question': question}
    return render(request, 'quiz_app/question.html', context)

def submit_answer(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        selected_option = request.POST.get('option')

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return redirect('get_question')

        session_id = request.session.get('quiz_session_id', None)
        if not session_id:
            return redirect('home')

        quiz_session = QuizSession.objects.get(session_id=session_id)

        # Add question to seen list
        quiz_session.add_seen_question(int(question_id))

        quiz_session.total_answered += 1
        if selected_option == question.correct_option:
            quiz_session.total_correct += 1
        else:
            quiz_session.total_incorrect += 1
        quiz_session.save()

        # Check if we've reached the question limit
        if quiz_session.total_answered >= quiz_session.question_limit:
            return redirect('quiz_result')
        else:
            return redirect('get_question')
    else:
        return redirect('home')

def quiz_result(request):
    session_id = request.session.get('quiz_session_id', None)
    if not session_id:
        return redirect('home')

    quiz_session = QuizSession.objects.get(session_id=session_id)
    total = quiz_session.total_answered
    correct = quiz_session.total_correct
    incorrect = quiz_session.total_incorrect

    accuracy = 0
    if total > 0:
        accuracy = (correct / total) * 100

    time_taken = None
    if quiz_session.start_time:
        time_taken = timezone.now() - quiz_session.start_time

    # You can also show from where questions are sourced. 
    # For demonstration, we’ll just note that they are from GeeksForGeeks.
    # If you want to list sources of answered questions, 
    # you'd need to store which questions were answered and retrieve their sources.

    context = {
        'quiz_session': quiz_session,
        'accuracy': accuracy,
        'time_taken': time_taken,
        'source': "https://www.geeksforgeeks.org/"
    }
    return render(request, 'quiz_app/dashboard.html', context)
