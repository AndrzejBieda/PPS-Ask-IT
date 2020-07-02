from django import forms
from pagedown.widgets import PagedownWidget

from Ask_IT.models import *


class QuestionContent(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Question
        fields = ["content"]