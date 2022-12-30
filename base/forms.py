from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User , Book


# Create your forms here.

class NewUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class NewBookForm(forms.ModelForm):
    # name = forms.CharField(max_length=100)
    # author = forms.CharField(max_length=100)
    # publisher = forms.CharField(max_length=100)
    
    # copies = forms.IntegerField()
    # coverpage = forms.CharField()
    class Meta:
        model = Book
        fields = '__all__'

    