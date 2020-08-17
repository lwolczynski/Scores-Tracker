from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordChangeForm
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

#New password form
class ResetPasswordForm(SetPasswordForm):
    new_password2 = forms.CharField(
        label="New password confirmation",
        help_text="Enter the same password as before, for verification.",
        strip=False,
        widget=forms.PasswordInput,
    )

#Change email form
class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(
        label="Current email address",
        widget=forms.EmailInput,
        disabled=True,
    )

    new_email1 = forms.EmailField(
        label="New email address",
        widget=forms.EmailInput,
    )

    new_email2 = forms.EmailField(
        label="New email address confirmation",
        widget=forms.EmailInput,
    )

    current_password = forms.CharField(
        label="Current password",
        help_text="Enter your current password for verification.",
        strip=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = CustomUser
        fields = ("email", "new_email1", "new_email2", "current_password")

    error_messages = {
        'email_mismatch': "The two email addresses fields didn't match.",
        'not_changed': "The email address is the same as the one already defined.",
    }

    def __init__(self, *args, **kwargs):
        super(EmailChangeForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.email
        except CustomUser.DoesNotExist:
            pass

    def clean_new_email1(self):
        old_email = self.instance.email
        new_email1 = self.cleaned_data.get('new_email1')
        if new_email1 and old_email:
            if new_email1 == old_email:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='not_changed',
                )
        return new_email1

    def clean_new_email2(self):
        new_email1 = self.cleaned_data.get('new_email1')
        new_email2 = self.cleaned_data.get('new_email2')
        if new_email1 and new_email2:
            if new_email1 != new_email2:
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch',
                )
        return new_email2

    def clean_current_password(self):
        valid = self.instance.check_password(self.cleaned_data['current_password'])
        if not valid:
            raise forms.ValidationError("Password incorrect.")
        return valid

    def save(self, commit=True):
        user = self.instance
        email = self.cleaned_data["new_email1"]
        user.email = email
        if commit:
            user.save()
        return user

#New password form
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current password",
        help_text="Enter your current password for verification.",
        strip=False,
        widget=forms.PasswordInput,
    )

    field_order = ['new_password1', 'new_password2', 'old_password']

# User personal data update form 
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    current_password = forms.CharField(
        label="Current password",
        help_text="Enter your current password for verification.",
        strip=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "current_password")

    def clean_current_password(self):
        valid = self.instance.check_password(self.cleaned_data['current_password'])
        if not valid:
            raise forms.ValidationError("Password incorrect.")
        return valid

# User personal data update form 
class UserDeleteForm(forms.ModelForm):
    current_password = forms.CharField(
        label="Current password",
        help_text="Enter your current password for verification.",
        strip=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = CustomUser
        fields = ("current_password", )

    def clean_current_password(self):
        valid = self.instance.check_password(self.cleaned_data['current_password'])
        if not valid:
            raise forms.ValidationError("Password incorrect.")
        return valid

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