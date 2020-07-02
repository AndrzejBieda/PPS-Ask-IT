from django import forms
from pagedown.widgets import PagedownWidget

from Ask_IT.models import *


class QuestionContent(forms.ModelForm):
    title = forms.CharField()
    content = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Question
        fields = ["title", "content"]
