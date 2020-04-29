from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.views import generic
from django.utils import timezone

# Create your views here.


# def index(request):
#
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     return render(request, 'polls/index.html', context=dict(latest_question_list=latest_question_list))


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


# def detail(request, question_id):
#
#     # try:
#     #     question = Question.objects.get(id=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404('question does not find')
#
#     question = get_object_or_404(Question, id=question_id)
#     return render(request, 'polls/detail.html', context=dict(question=question))


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


# def results(request, question_id):
#     question = get_object_or_404(Question, question_id)
#
#     return render(request, 'polls/results.html', context=dict(question=question))


class ResultsView(generic.DetailView):
    template_name = 'polls/results.html'
    model = Question


def votes(request, question_id):

    question = get_object_or_404(Question, id=question_id)

    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',
                      context=dict(question=question, error_message="You did not select any..."))

    selected_choice.votes += 1
    selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
