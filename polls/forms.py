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

    def is_valid(self):
        super(QuestionForm, self)
        sch = self.data.get('ch', 0)
        return sch <> 0
        
    def save(self, commit=False):
        question = super(QuestionForm, self).save(False)
        sch = self.data.get('ch', 0)
        selected_choice = question.choice_set.get(pk=sch)
        selected_choice.votes += 1
        selected_choice.save()
        return question
    
    
