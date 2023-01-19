from django.test import TestCase
from django.urls import reverse
from datetime import timedelta, datetime

from .models import Question

def create_question(text, days, num_of_choices = 2):
    question = Question.objects.create(question_text = text, pub_date = datetime.now()+timedelta(days=days))
    for _ in range(num_of_choices):
        question.choice_set.create(choice_text = 'don\'t care')
    return question

class QuestionIndexViewTest(TestCase):

    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_past_question(self):
        question = create_question(text = "Past question", days = -2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions'], [question,])

    def test_future_question(self):
        create_question(text='Future question', days=2)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_questions'], [])
    
    def test_future_and_past(self):
        create_question(text='future', days=2)
        question = create_question(text='past', days=-35)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions'], [question,])

    def test_past_2x(self):
        question1 = create_question(text='first', days=-1)
        question2 = create_question(text='second', days=-2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions'], [question1, question2])

    def test_lt_2_choices(self):
        create_question(text='do not care', days=-2, num_of_choices=1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions'], [])
    

class TestDetailView(TestCase):
    
    def test_future_questions(self):
        question = create_question(text="should not be displayed", days=3)
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_published_questions(self):
        question = create_question(text='already exist', days=0)
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)

    def test_lt_2_choises(self):
        question = create_question(text='not important', days=-2, num_of_choices=1)
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertEqual(response.status_code, 404)




class TestQuestions(TestCase):

    def test_for_future_questions_in_recently_published(self):
        future_question = Question(pub_date = datetime.now()+timedelta(seconds=1))
        self.assertIs(future_question.was_published_recently(), False)

    def test_for_old_questions_in_recently_published(self):
        old_question = Question(pub_date = datetime.now()+timedelta(days=1))
        self.assertIs(old_question.was_published_recently(), False)
    
    def test_for_recent_questions_in_recently_published(self):
        recent_question = Question(pub_date = datetime.now()+timedelta(days=1, seconds=-1))
        self.assertIs(recent_question.was_published_recently(), False)