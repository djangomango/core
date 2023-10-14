from django.apps import AppConfig


class PageConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    label = "page"
    name = "apps.page"

    @staticmethod
    def model_imports():
        import apps.page.models  # noqa

    @staticmethod
    def signal_imports():
        pass

    def ready(self):
        self.model_imports()
        self.signal_imports()