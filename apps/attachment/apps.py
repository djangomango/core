from django.apps import AppConfig


class AttachmentConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    label = "attachment"
    name = "apps.attachment"

    @staticmethod
    def model_imports():
        import apps.attachment.models  # noqa

    @staticmethod
    def signal_imports():
        pass

    def ready(self):
        self.model_imports()
        self.signal_imports()