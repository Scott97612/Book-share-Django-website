from django import forms
from .models import Title,Entry

class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = ['text']
        labels = {'text':''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text':''}
        widgets = {'text': forms.Textarea(attrs={'cols':80})}