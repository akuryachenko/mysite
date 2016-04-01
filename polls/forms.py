from django import forms
from .models import Choice, Question

class QuestionForm(forms.Form):
    ch = forms.ModelChoiceField(empty_label=None, label = '', widget=forms.RadioSelect, queryset=Choice.objects.all())

    def __init__(self, instance, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['ch'].queryset = instance.choice_set.all()            
