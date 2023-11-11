from django import forms

class RepositoryForm(forms.Form):
    repositories = forms.ChoiceField(choices=[], required=False)