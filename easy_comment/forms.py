from django import forms
from django.template.defaultfilters import striptags
from .models import Comment

class CommentForm(forms.ModelForm):
    honeypot = forms.CharField(required=False,
                               label='If you enter anything in this field, you comment will be treated as spam!')
    class Meta:
        model = Comment
        fields = ('content', 'parent', 'post')
        error_messages = {
            'content': {
                'empty': 'Some useful help text.',
            },
        }

    def clean_content(self):
        value = self.cleaned_data['content']
        if striptags(value).replace(' ', '').replace('&nbsp;', '') == '' and not '<img' in value:
            self.add_error('content', '兄dei，评论内容不能为空~')
        return value