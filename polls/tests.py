"""Tests of Django polls application for authentication using Django pytest."""
from django.test import TestCase
import datetime
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Question
import django.test


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(
            hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_can_vote_in_future(self):
        """test poll Can vote, if poll doesn't open. It should be return False """
        time = timezone.now() + datetime.timedelta(
            hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.can_vote(), False)

    def test_can_vote_correctly_current_time(self):
        """test when pub_date of poll is correctly a current time"""
        time = timezone.now()
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.can_vote(), True)

    def test_is_published(self):
        """test function is_published by it Return true when poll is opened."""
        time = timezone.now() - datetime.timedelta(
            hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.is_published(), True)

    def test_can_vote_end_date(self):
        """test when end_date of poll is correctly a current time"""
        time = timezone.now()
        recent_question = Question(
            pub_date=time - datetime.timedelta(minutes=59, seconds=59))
        self.assertIs(recent_question.can_vote(), True)

    def test_can_vote_poll_expired(self):
        """test poll Can vote, if poll expired. It should be return False """
        time = timezone.now()
        recent_question = Question(
            pub_date=time - datetime.timedelta(
                hours=24, minutes=59, seconds=59),
            end_date=time - datetime.timedelta(
                hours=2, minutes=59, seconds=59))
        self.assertIs(recent_question.can_vote(), False)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 302 not found.
        """
        future_question = create_question(
            question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(
            question_text='Past Question.', days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class UserAuthTest(django.test.TestCase):
    """Tests of authentication."""

    def setUp(self):
        """Superclass setUp creates a Client object and initializes database."""
        super().setUp()
        self.username = "rew1233"
        self.password = "Admin1234@"
        self.user1 = User.objects.create_user(
            username=self.username,
            password=self.password,
            email="yo@gmail.com")
        self.user1.first_name = "rewkub"
        self.user1.save()

    def test_login_view(self):
        """Test that a user can login via the login view."""
        login_url = reverse("login")
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        data_user = {"username": "rew1233",
                     "password": "Admin1234@"
                     }
        response = self.client.post(login_url, data_user)
        self.assertEqual(302, response.status_code)
        self.assertEqual('/polls/', reverse("polls:index"))
        self.assertRedirects(response, reverse("polls:index"))
