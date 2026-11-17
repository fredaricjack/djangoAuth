
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserForm(forms.ModelForm):

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Create a strong password',
                'autocomplete': 'new-password'
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter your username'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address'
            }),
        }

    def clean_email(self):

        email = self.cleaned_data['email'].strip()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'This email address is already registered.'
            )

        return email

    def clean_password(self):

        password = self.cleaned_data['password']

        validate_password(password)

        return password
