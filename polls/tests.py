import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question, Choice
from django.urls import reverse


# Create your tests here.


class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)

        future_date = Question(pub_date=time)

        self.assertIs(future_date.was_publish_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)

        future_date = Question(pub_date=time)

        self.assertIs(future_date.was_publish_recently(), False)

    def test_was_published_recently_with_recently_question(self):
        time = timezone.now() - datetime.timedelta(minutes=10)

        future_date = Question(pub_date=time)

        self.assertIs(future_date.was_publish_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexTest(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have no question')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        create_question(question_text='past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: past question>']
        )

    def test_future_question(self):
        create_question(question_text='future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'You have no question')
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            []
        )


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        # response = self.client.get(reverse('polls:detail', args=future_question.id))
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        # print(url)
        # print(response)

        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='past question.', days=-5)
        # response = self.client.get(reverse('polls:detail', args=future_question.id))
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        # print(url)
        # print(response)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)
