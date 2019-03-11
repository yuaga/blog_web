from django import forms
from apps.forms import FormMixin
from . import models


# class EditCategoryForm(forms.Form, FormMixin):
#     name = forms.CharField(max_length=6, error_messages={"max_length": "输入的分类超过了6个字符，请重新编辑！"})


class WriteNewsForm(forms.ModelForm, FormMixin):

    class Meta:
        model = models.News
        exclude = ['pub_time', 'author']


class EditNewsForm(forms.ModelForm, FormMixin):
    id = forms.IntegerField()

    class Meta:
        model = models.News
        exclude = ['author', 'pub_time']
