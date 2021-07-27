#Required Packages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from rest_framework.decorators import api_view
import requests
import json
from urllib import parse as urlparse
import sys

#Add Path
sys.path.append("./polls/src/")

#Internal Packages
from .models import Question, Choice
from utils import fun

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@api_view(["GET", "POST"])
def test(request):
	if request.method == "POST":
		#Unpack Parameters
		params = json.loads(request.body.decode("utf-8"))
		number = params["number"]
	
		#Run add_two Function
		answer = fun.add_two(number)

		#Compile Response Object
		response = json.dumps(
		{"request.method" : request.method,
		"your_input"      : number,
		"add_two_result"  : answer}
		)
	
	else:
		response = json.dumps({"error" : "wrong request method used; use POST"})

	return HttpResponse(response, content_type="application/json")

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected.votes += 1
        selected.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
