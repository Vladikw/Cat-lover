from django import forms
from .models import User, UserPhoto
from django.contrib.auth.hashers import make_password


class RegisterUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields.pop('password', None)
            self.fields.pop('password2', None)

    password = forms.CharField(
        label='Пароль',
        max_length=24,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        max_length=24,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        }),
        help_text='Введите тот же пароль ещё раз для подтверждения.',
    )

    class Meta:
        model = User
        fields = ['login', 'email', 'name', 'address', 'telephone']
        labels = {
            'login': 'Логин',
            'email': 'E-mail',
            'name': 'Имя',
            'address': 'Адрес',
            'telephone': 'Телефон',
        }
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите телефон'}),
        }

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)

        # Если пароль есть в cleaned_data (значит, форма используется при создании)
        if 'password' in self.cleaned_data:
            user.password = make_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user


class RegisterUserPhotoForm(forms.ModelForm):
    class Meta:
        model = UserPhoto
        fields = ['photo']
        labels = {
            'photo': 'Фотография',
        }
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
