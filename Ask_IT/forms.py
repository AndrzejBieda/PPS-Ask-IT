from django import forms


class QuestionContent(forms.Form):
    content = forms.CharField()
