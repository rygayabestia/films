from django import forms
from .models import User

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'login', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = self.cleaned_data['password']  # Сохраняем пароль в явном виде
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'login', 'password')