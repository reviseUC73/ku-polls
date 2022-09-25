from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question, Vote
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(generic.ListView):
    """View for index.html."""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    """View for detail.html page"""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, pk):
        """
        when your website can't found poll or this poll expired ,
        it come to main poll page
        """
        user = request.user
        question = get_object_or_404(Question, pk=pk)
        try:
            self.question = Question.objects.get(pk=pk)
            if self.question.can_vote():
                select_vote = ''
                user_poll_vote = Vote.objects.filter(user=user)
                for select in user_poll_vote:
                    if select.question == question:
                        select_vote = select.choice.choice_text

                return render(request, 'polls/detail.html',
                              {'question': self.question,
                               "select_vote": select_vote})
            else:
                messages.error(request,
                               "The poll can't vote at this time.")
                return HttpResponseRedirect(reverse('polls:index'))
        except Question.DoesNotExist:
            messages.error(request, "This poll has not this question")
            return HttpResponseRedirect(reverse('polls:index'))


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """
    Add vote to choice of the current question.
    """
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
        # return redirect('/accounts/login/')
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(
            pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        user = request.user
        try:
            votes = Vote.objects.filter(user=user).filter(
                choice__question=question)
            if votes.count() == 0:
                vote = selected_choice.vote_set.create(
                    user=user, question=question)
            else:
                vote = votes[0]
                vote.choice = selected_choice
        except Vote.DoesNotExist:
            vote = selected_choice.vote_set.create(
                user=user, question=question)

        vote.save()

        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))
