from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from .models import CustomUser, HolesNumber, Sport, Game

TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)

#Register form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required.')

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

#Forgot password form
class ForgotPasswordForm(PasswordResetForm):
    pass

#New password form
class ResetPasswordForm(SetPasswordForm):
    new_password2 = forms.CharField(
        label="New password confirmation",
        help_text="Enter the same password as before, for verification.",
        strip=False,
        widget=forms.PasswordInput,
    )

#New game form
class NewGameForm(ModelForm):
    sport = forms.Select(
        choices = Sport.objects.all().values_list('id', 'name')
    )
    holes = forms.Select(
        choices = Sport.objects.all().values_list('id', 'name')
    )

    class Meta:
        model = Game
        fields = ("sport", "holes")

    #Sport validation
    def clean_renewal_sport(self):
        data = self.cleaned_data['sport']
        valid_types = Sport.objects.all().values_list('id')
        if data not in valid_types:
            raise ValidationError('Pick valid type!')

        # Remember to always return the cleaned data.
        return data
    
    #Holes validation
    def clean_renewal_holes(self):
        data = self.cleaned_data['holes']
    
        data = self.cleaned_data['holes']
        valid_types = Sport.objects.all().values_list('id')
        if data not in valid_types:
            raise ValidationError('Pick valid type!')

        # Remember to always return the cleaned data.
        return data