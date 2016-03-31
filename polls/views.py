from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F, Count
from django.utils import timezone
from django.conf import settings
from django.conf.urls.static import static
from random import choice as random_choice

from .models import Choice, Question, CUserChoice
from .forms import *

class IndexView(generic.UpdateView):
    model = Question
    template_name = 'polls/index.html'
    form_class = QuestionForm

    def get_queryset(self):
        question = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        if self.request.user.is_authenticated():
            q_u = CUserChoice.objects.filter(cuser=self.request.user).values('choice__question')
            return question.exclude(id__in=q_u)
        else:
            return question

    def get_object(self, queryset=None):
        questions = self.get_queryset()
        if questions:
            magic_question_id = random_choice([q.id for q in questions])
            return Question.objects.get(id=magic_question_id)
        else:
            return None    

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['question_list'] = self.get_queryset()
        return context
    
    def form_valid(self, form):
        sch = form.cleaned_data['ch'].id
        context = self.get_context_data()
        
        if self.request.user.is_authenticated():
            choice = Choice.objects.get(pk=sch)
            user_choice = CUserChoice(choice=choice, cuser=self.request.user, date_vote = timezone.now())
            user_choice.save()
            return HttpResponseRedirect(reverse('detail', args=(context['question'].id,))) 
                       
        else:
            self.request.session['anonym_vote'] = sch
            return HttpResponseRedirect(reverse('registration'))
    
    
class UserResultsView(generic.ListView):
    
    template_name = 'polls/userresults.html'
    context_object_name = 'list_results'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise Http404("Not authenticated user")
        return super(UserResultsView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return CUserChoice.objects.filter(cuser=self.request.user).select_related('choice__question','choice' )
        return None    

       
class DetailView(generic.UpdateView):
    model = Question
    template_name = "polls/detail.html"
    form_class = QuestionForm
      
    def get_queryset(self):
        question = super(DetailView, self).get_queryset().filter(pub_date__lte=timezone.now())
        return question
    
    def dispatch(self, request, *args, **kwargs):
        request.session.delete('anonym_vote')
        return super(DetailView, self).dispatch(request, *args, **kwargs)       
            
    def form_valid(self, form):
        sch = form.cleaned_data['ch'].id
        if self.request.user.is_authenticated():
            #Choice.objects.filter(pk=sch).update(votes=F('votes') + 1)
            choice = Choice.objects.get(pk=sch)
            user_choice = CUserChoice(choice=choice, cuser=self.request.user, date_vote = timezone.now())
            user_choice.save()
            
            #results
            context = self.get_context_data()
            return render(self.request, 'polls/detail_results.html', context)
                       
        else:
            self.request.session['anonym_vote'] = sch
            return HttpResponseRedirect(reverse('registration'))
    
    def get_template_names(self):
        template_name =  super(DetailView, self).get_template_names()
        if not self.request.user.is_authenticated():
            return template_name
        else:
            q_u = CUserChoice.objects.filter(cuser=self.request.user).values('choice__question')
            if q_u.filter(choice__question=self.object.id).count() > 0:
                return ['polls/results.html']      
                
            return template_name

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        
        if self.request.user.is_authenticated():
            question = context['question']
            print question

            choices = Choice.objects.filter(question=question).values('id') #all().cuserchoice_set(cuser=self.request.user).all().first()
            vote = CUserChoice.objects.filter(cuser=self.request.user).values('choice')
            choice = choices.filter(id__in=vote).first()

            choice_id = choice['id'] if choice else None
                
            votes = question.choice_set.all().annotate(num=Count('cuserchoice'))
           
            user_votes = [{'text': v.choice_text, 'num': v.num, 'per': 0, 'b': True if v.id==choice_id else False} for v in votes]
            
            sum_votes = 0
            for i in user_votes:
                sum_votes = sum_votes + i['num']
            
            if sum_votes > 0:
                for i in user_votes:
                    i['per'] = i['num']* 100 / sum_votes
            
            context['user_votes'] = user_votes
            
        return context
        
        
    

