from django import forms
from .models import Choice, Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text',)
        widgets = { 'question_text': forms.HiddenInput,}
    
    ch = forms.ModelChoiceField(empty_label=None, label = '', widget=forms.RadioSelect, queryset=Choice.objects.all())
        
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        question = self.instance 
        self.fields['ch'].queryset = question.choice_set.all()
        #self.fields['ch'].label = question.question_text

    def save(self, commit=False):
        question = super(QuestionForm, self).save(False)
        sch = self.fields['ch'].widget.choices[2] #self.request.POST['ch']
        selected_choice = question.choice_set.get(pk=sch)
        selected_choice.votes += 1
        selected_choice.save()
        return question
    
    
