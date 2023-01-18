from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from polls.models import Choice, Question


class Index(generic.ListView):
    context_object_name = 'latest_5_questions'
    template_name = 'polls/index.html'

    def get_queryset(self):
        """Return the last 5 published questions
        (not including those set to be published in the future)"""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class Detail(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class Results(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    # shortcut for the pattern try + .objects.get + except
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
