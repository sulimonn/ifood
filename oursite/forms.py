from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import time
from .models import *


User._meta.get_field('email')._unique = True


def random_username(instance, **kwargs):
    if not instance.username:
        instance.username = 'id' + str(int(time.time() * 10000 % 100000000))


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=30)
    email = forms.EmailField(label='Адрес эл.почты')
    field_order = ['first_name', 'email', 'password1']

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password1']

        labels = {
            'password1': 'Пароль',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.Meta.labels.items():
            self[k].label = v
        self.fields['first_name'].widget.attrs["class"] = 'translate'
        self.fields['email'].widget.attrs["class"] = 'translate'
        self.fields['password1'].widget.attrs["class"] = 'translate'
        del self.fields['password2']

    models.signals.pre_save.connect(random_username, sender=User)


class LoginForm(AuthenticationForm):
    email = forms.EmailField(label='Адрес эл.почты')
    field_order = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields.pop('username')
        self.fields['email'].widget.attrs["class"] = 'translate'
        self.fields['password'].widget.attrs["class"] = 'translate'

    def clean(self):
        user = User.objects.get(email=self.cleaned_data.get('email'))
        self.cleaned_data['username'] = user.username
        return super(LoginForm, self).clean()
