from django.forms import ModelForm
from .models import CaseLog


class CaseLogCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["case"].disabled = True
        self.fields["author"].disabled = True

    class Meta:
        model = CaseLog
        fields = ["title", "case", "author", "body"]
