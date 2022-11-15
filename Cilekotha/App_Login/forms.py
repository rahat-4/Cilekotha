from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from App_Login.models import User, Profile
# User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', )