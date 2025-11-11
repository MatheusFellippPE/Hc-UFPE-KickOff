try:
    from django.apps import AppConfig
except ModuleNotFoundError:
    # Django não está disponível no ambiente atual.
    class AppConfig:  # stub mínimo para evitar que linters quebrem
        pass

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
