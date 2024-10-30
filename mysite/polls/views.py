
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question

import logging

logger = logging.getLogger(__name__)

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"



def vote(request, question_id):
    logger.info(f'Vote attempt for question_id: {question_id} by user: {request.user}')
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        logger.info(f'Selected choice: {selected_choice}')
    except (KeyError, Choice.DoesNotExist):
        logger.error('No choice selected or choice does not exist.')
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        logger.info(f'Vote counted for choice: {selected_choice}')
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    return redirect('polls:index')