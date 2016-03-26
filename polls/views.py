from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F, Count
from django.utils import timezone
from django.conf import settings
from django.conf.urls.static import static


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
    
       
class DetailView(generic.UpdateView):
    model = Question
    template_name = 'polls/detail.html'
    form_class = QuestionForm
      
    
    def get_queryset(self):
        question = super(DetailView, self).get_queryset().filter(pub_date__lte=timezone.now())
        return question
    
    def get_object(self, queryset=None):
        question = super(DetailView, self).get_object()
        if self.request.user.is_authenticated():
            q_u = CUserChoice.objects.filter(cuser=self.request.user).values('choice__question')
            
            if q_u.filter(choice__question=question.id).count() > 0:
                print "-------------------------------"
                print q_u.filter(choice__question=question.id).count()
                reverse('index')
                
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
            
            # ---------results
            context = self.get_context_data()
            question = context['question']
            votes = question.choice_set.all().annotate(num=Count('cuserchoice'))
            
            user_votes = [{'text': v.choice_text, 'num': v.num, 'per': 0, 'b': True if v.id==sch else False} for v in votes]
            
            sum_votes = 0
            for i in user_votes:
                sum_votes = sum_votes + i['num']
                
            for i in user_votes:
                i['per'] = i['num']* 100 / sum_votes
                                
            context['user_votes'] = user_votes
            return render(self.request, 'polls/results.html', context)
                       
        else:
            self.request.session['anonym_vote'] = sch
            return HttpResponseRedirect('/')

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            raise Http404("User is anonymous")
        return super(ResultsView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        question = context['question']
        context['user_votes'] = question.choice_set.all().annotate(num=Count('cuserchoice'))
        print question
        return context
    
    def get_queryset(self):        
        qs = super(ResultsView, self).get_queryset()
        return qs.filter(pub_date__lte=timezone.now())
    

