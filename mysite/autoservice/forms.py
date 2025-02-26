from django.contrib.auth.models import User
from .models import Profile, Order

from .models import OrderComment
from django import forms

class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = OrderComment
        fields = ['content']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']

class MyDateTimePicker(forms.DateInput):
    input_type = "datetime-local"

class OrderCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['car', 'deadline']
        widgets = {'deadline': MyDateTimePicker()}