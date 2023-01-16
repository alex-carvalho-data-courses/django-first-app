from django.http import (
    HttpResponse, HttpRequest, Http404, HttpResponseRedirect
)
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from polls.models import Choice, Question


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
    # shortcut for the pattern try + .objects.get + except used at detail()
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question,
            'error_message': "You didn't select a choice."
        }
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()

        # Always return an HttpResponseRedirect after successfully dealing with
        # POST data. This prevents from data being posted twice if the user
        # hits the Back button.
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))
        # HttpResponseRedirect() receives an URL as parameter
        # reverse() receives a view name and a parameter and returns the URL
        # the example above will return something like '/polls/2/results/'
