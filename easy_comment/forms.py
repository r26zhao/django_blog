from django import forms
from .models import *

class CommentForm(forms.ModelForm):
    honeypot = forms.CharField(required=False,
                               label='If you enter anything in this field, you comment will be treated as spam!',)
    class Meta:
        model = Comment
        fields = ('content', 'parent')

    def clean_honeypot(self):
        value = self.cleaned_data['honeypot']
        if value:
            raise forms.ValidationError(self.fields['honeypot'].label)
        return value

    def clean_content(self):
        value = self.cleaned_data['content']
        print(value.replace('&nbsp;', ''))
        if value.replace('&nbsp;', '') == '<p></p>':
            raise forms.ValidationError('评论不能为空！')
        return value