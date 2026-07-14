from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import User


class InscriptionForm(forms.ModelForm):
    """Formulaire d'inscription PokéMarket."""

    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ['pseudo', 'email']

    def clean_password1(self):
        """Vérifie que le mot de passe est assez solide."""
        password1 = self.cleaned_data.get('password1')
        validate_password(password1)
        return password1

    def clean(self):
        """Vérifie que les deux mots de passe sont identiques."""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Les mots de passe ne correspondent pas."
            )
        return cleaned_data

    def save(self, commit=True):
        """Sauvegarde l'utilisateur avec is_active=False."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False  # bloqué jusqu'à confirmation email
        user.username = self.cleaned_data['email']  # username = email
        if commit:
            user.save()
        return user


class ChangerEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'ton@email.com'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(
            email=email
        ).exists():
            raise forms.ValidationError(
                "Cet email est déjà utilisé par un autre compte."
            )
        return email
