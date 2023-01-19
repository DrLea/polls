from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F, Count
from django.views import generic
from django.utils import timezone


from .models import Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        return list(filter(lambda question: question.has_options(), questions))[:5]


class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    model = Question

    def get_queryset(self):
        published = Question.objects.filter(pub_date__lte=timezone.now())
        annotated = published.annotate(number_of_choices=Count('choice'))
        return annotated.filter(number_of_choices__gte=2)
    


class ResultsView(generic.DetailView):
    template_name = 'polls/result.html'
    model = Question

    def get_queryset(self):
        published = Question.objects.filter(pub_date__lte=timezone.now())
        annotated = published.annotate(number_of_choices=Count('choice'))
        return annotated.filter(number_of_choices__gte=2)

def results(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    response = [{choice.choice_text: choice.votes} for choice in question.choice_set.all()]
    return JsonResponse({question.question_text:response})

def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except:
        return render(request, 'polls/detail.html',\
        {'question':question, 'error_message':'You did not choose the answer'})
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))