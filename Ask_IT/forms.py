from django import forms
from pagedown.widgets import PagedownWidget

from Ask_IT.models import Question


class QuestionContent(forms.Form):
    content = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Question
        fields = ["content"]
