from django.forms import ModelForm
from test_app.models import Devoir
class DevoirForm(ModelForm):
    class Meta:
     model=Devoir
     fields=['name','file_dev']