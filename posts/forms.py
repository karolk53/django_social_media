from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from .models import PostComment


class PostCommentForm(ModelForm):

    class Meta:
        model = PostComment
        fields = ["contents"]

    def __int__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"

