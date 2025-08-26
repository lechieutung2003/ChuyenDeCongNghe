from django import forms

from myapp.models import LogMessage


class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ("message",)
