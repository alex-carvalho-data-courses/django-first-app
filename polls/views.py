from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render
from django.template import loader
from polls.models import Question


def index(request: HttpRequest) -> HttpResponse:
    latest_5_questions = Question.objects.order_by('-pub_date')[:5]

    template = loader.get_template('polls/index.html')
    context = {
        'latest_5_questions': latest_5_questions
    }

    return HttpResponse(template.render(context, request))


def detail(request: HttpRequest, question_id: int) -> HttpResponse:
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')

    # shortcut for the approach used in index() - loader + template.render()
    # + HttpResponse
    return render(request, 'polls/detail.html', {'question': question})


def results(request: HttpRequest, question_id: int) -> HttpResponse:
    return HttpResponse(f"You're looking at the results of question "
                        f"{question_id}.")


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    return HttpResponse(f"You're voting on question {question_id}.")