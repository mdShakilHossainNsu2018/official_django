from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Question, Choice

# Create your views here.


def index(request):

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    return render(request, 'polls/index.html', context=dict(latest_question_list=latest_question_list))


def detail(request, question_id):

    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404('question does not find')

    return render(request, 'polls/detail.html', context=dict(question=question))


def results(request, question_id):
    return HttpResponse(f'You\'re looking at the results of question {question_id}')


def votes(request, question_id):
    return HttpResponse(f'You\'re looking at the votes of question {question_id}')
