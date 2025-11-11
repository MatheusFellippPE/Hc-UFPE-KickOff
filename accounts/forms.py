import re
from django import forms

PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&._-])[A-Za-z\d@$!%*#?&._-]{8,}$"
)
PASSWORD_HELP = "Mín. 8 caracteres, com letra maiúscula, minúscula, número e caractere especial."

class RegistrationForm(forms.Form):
    name = forms.CharField(label="Nome completo", max_length=150)
    email = forms.EmailField(label="Email")
    user_type = forms.ChoiceField(choices=[
        ("aluno", "Aluno"),
        ("professor", "Professor"),
        ("pesquisador", "Pesquisador"),
        ("outro", "Outro"),
    ], label="Tipo de usuário")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput, help_text=PASSWORD_HELP)
    password_confirmation = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)

    def clean_password(self):
        pwd = self.cleaned_data.get("password", "")
        if not PASSWORD_REGEX.match(pwd):
            raise forms.ValidationError(PASSWORD_HELP)
        return pwd

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password")
        p2 = cleaned.get("password_confirmation")
        if p1 and p2 and p1 != p2:
            self.add_error("password_confirmation", "As senhas não coincidem.")
        return cleaned

class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
