from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from django.contrib import messages


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    # def get_queryset(self):
    #     """
    #     Excludes any questions that aren't published yet.
    #     """
    #     return Question.objects.filter(pub_date__lte=timezone.now())

    # def get(self, request, pk_id=None):
    #     question = get_object_or_404(Question, pk=pk_id)
    #     # print("rew")
    #     if not question.can_vote():
    #         messages.error(request, f"Yo man you can't vote on \"{question.question_text}\" poll anymore its to late. "
    #                        f"\U0001F612")
    #         return HttpResponseRedirect(reverse('polls:index'))
    #     else:
    #         return render(request, 'polls/detail.html', {'question': question, })
    
    # def get(self, request, pk):
    #     """Return different pages in accordance to can_vote and is_published."""
    #     question = get_object_or_404(Question, pk=pk)
    #     if not question.can_vote():
    #         messages.error(request, 'This poll not publish yet.')
    #         return HttpResponseRedirect(reverse('polls:index'))
    #     elif not question.can_vote():
    #         messages.error(request, 'This poll is ended.')
    #         return HttpResponseRedirect(reverse('polls:results', args=(pk,)))
    #     else:
    #         return render(request, 'polls/detail.html', {'question': question, })




class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
