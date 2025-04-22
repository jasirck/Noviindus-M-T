from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from users.models import CustomUser


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'status', 'completion_report', 'worked_hours']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'completion_report': forms.Textarea(attrs={'rows': 3}),
        }


class UserTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'status', 'completion_report', 'worked_hours']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'rows': 3, 'readonly': 'readonly'}),
            'completion_report': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(UserTaskForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].disabled = True
        self.fields['title'].disabled = True
        self.fields['description'].disabled = True
        self.fields['due_date'].disabled = True



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'is_superuser']
        labels = {
            'is_superuser': 'Is Admin',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Specific placeholders for password fields
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})


class EditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'is_superuser']
        labels = {
            'is_superuser': 'Is Admin',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 transition'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 transition'}),
            'role': forms.Select(choices=CustomUser.ROLE_CHOICES, attrs={'class': 'w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 transition'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'mr-2 rounded'}),
        }

