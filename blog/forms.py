from django.forms import ModelForm
from .models import User

class UserDetailForm(ModelForm):
    class Meta:
        model = User
        fields = ('nickname', 'qq', 'url', 'avatar')