from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        exclude = ['user']  # 🚫 We don’t want to show user in the form
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),  # 📅 HTML date picker
        }
