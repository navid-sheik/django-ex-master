
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import InlineCheckboxes

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Row, Layout, Submit
# from crispy_forms.bootstrap import FormActions
#from .models import Profile
from django.contrib.auth import get_user_model

from django.contrib.admin import widgets
from django.db import models
from django.db.models import fields
from django.forms import Form, ModelForm
from django.forms.widgets import DateInput

from mainapp.models import Hobby, Profile
User = get_user_model()

class UserRegisterForm(UserCreationForm):
#   email = forms.EmailField()
 
  class Meta:
      model = User
      fields =  ['username', 'email', 'password1', 'password2']
      widgets = {
            'dob' : DateInput(attrs={'type': 'date'}),
        }

 
    
class ProfileForm (forms.ModelForm):
    class Meta:
        model =  Profile
        # fields =  ['dob', 'city', 'age']
        fields =  ['dob', 'city']
        widgets = {
            'dob' : DateInput(attrs={'type': 'date'}),
        }

class ProfilePicForm (forms.ModelForm):
    class Meta:
        model =  Profile
        fields =  ['image']
        widgets = {
            'dob' : DateInput(attrs={'type': 'date'}),
        }


        
class UpdateUserEmailForm (forms.ModelForm):
    class Meta:
        model = User
        fields =  [ 'email']

    # helper = FormHelper()
    # helper.layout = Layout(
    #     Row('username', css_class="mb-2"),
    #     Row('password', css_class="mb-2"),
    #     FormActions(
    #         Submit('login', 'Log in', css_class="mt-2"),
    #     )
    # )



class HobbiesMultiForm(forms.Form):
    hobby = forms.ModelMultipleChoiceField(queryset=Hobby.objects.all(),widget=forms.CheckboxSelectMultiple)
    def __init__(self, *args, **kwargs):
        super(HobbiesMultiForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            InlineCheckboxes('hobby')
        )

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']


# class ProfileUpdateForm(forms.ModelForm):
# 	class Meta:
# 		model = Profile
# 		fields = ['city', 'dob']