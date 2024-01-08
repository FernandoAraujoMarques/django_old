from django import forms
from .models import Member

class StatusForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['status']
