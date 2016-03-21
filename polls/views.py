from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F
from django.utils import timezone

from .models import Choice, Question, CUserChoice
from .forms import *

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        question = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        
        if self.request.user.is_authenticated():
            q_u = CUserChoice.objects.filter(cuser=self.request.user).values('choice__question')
            return question.exclude(id__in=q_u)[:5]
        else:
            return question[:5]
    
    def get_success_url(self):
        return reverse('results', args=(self.object.id,))   
    

        
class DetailView(generic.UpdateView):
    model = Question
    template_name = 'polls/detail.html'
    form_class = QuestionForm
    #success_url = 'results/'     
    
    def get_queryset(self):
        qs = super(DetailView, self).get_queryset()
        return qs.filter(pub_date__lte=timezone.now())
    
            
    def form_valid(self, form):
        sch = form.cleaned_data['ch'].id
        if self.request.user.is_authenticated():
            Choice.objects.filter(pk=sch).update(votes=F('votes') + 1)
            choice = Choice.objects.get(pk=sch)
            user_choice = CUserChoice(choice=choice, cuser=self.request.user, date_vote = timezone.now())
            user_choice.save()
            return HttpResponseRedirect(reverse('results', args=(self.object.id,)))
        else:
            return HttpResponseRedirect(reverse('registration', args=(sch,)))

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



