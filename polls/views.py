from django.http import HttpResponse, HttpRequest
from polls.models import Question


def index(request: HttpRequest) -> HttpResponse:
    latest_5_questions = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_5_questions])

    return HttpResponse(output)


def detail(request: HttpRequest, question_id: int) -> HttpResponse:
    return HttpResponse(f"You're looking at question {question_id}.")


def results(request: HttpRequest, question_id: int) -> HttpResponse:
    return HttpResponse(f"You're looking at the results of question "
                        f"{question_id}.")


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    return HttpResponse(f"You're voting on question {question_id}.")