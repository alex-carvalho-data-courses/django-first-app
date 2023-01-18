import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


def create_question(question_text: str, days_offset: int) -> Question:
    """
    Creates a Question with a given 'question_text' and published the given
    number of 'days' offset to now (negative for questions published in the
    past, positive for questions that have yet to be published.
    """
    publish_date = timezone.now() + datetime.timedelta(days=days_offset)
    return Question.objects.create(
        question_text=question_text,
        pub_date=publish_date
    )


class QuestionDetailViewTest(TestCase):

    def test_future_question(self) -> None:
        """
        The detail view of question with pub_date in the future should return
        a 404 not found
        """
        future_question = create_question('how was yesterday?', 1)
        url = reverse('polls:detail', args=[future_question.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self) -> None:
        """
        The detail view of question with pub_date in the past displays the
        question's text.
        """
        past_question = create_question('who died?', -1)
        url = reverse('polls:detail', args=[past_question.id])
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self) -> None:
        """
        If no Questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_5_questions'], [])

    def test_past_question(self) -> None:
        question = create_question('Ser ou nao ser?', -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_5_questions'],
            [question]
        )

    def test_no_questions_again(self) -> None:
        """
        If no Questions exist, an appropriate message is displayed.
        (This test is to check if the DB is recreated for every test)
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_5_questions'], [])

    def test_future_question(self) -> None:
        create_question('posso pagar fiado?', 1)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_5_questions'], [])

    def test_future_and_past_question(self) -> None:
        past_question = create_question('quem manda?', -10)
        create_question('o que é melhor nem perguntar?', 10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_5_questions'],
            [past_question]
        )

    def test_two_past_questions(self) -> None:
        question_1 = create_question('how to start?', -10)
        question_2 = create_question('how to finish?', -20)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_5_questions'],
            [question_1, question_2]
        )


class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_question(self) -> None:
        """
        was_published_recently() should return False for questions w
        hose pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self) -> None:
        """
        was_published_recently() should return False for questions
        whose pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=2)
        old_question = Question(pub_date=time)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self) -> None:
        """
        was_published_recently should return True for Questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=8)
        recent_question = Question(pub_date=time)

        self.assertIs(recent_question.was_published_recently(), True)