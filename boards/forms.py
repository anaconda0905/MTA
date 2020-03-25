from django import forms
from .models import Post, Topic


class NewTopicForm(forms.ModelForm):
    subject = forms.CharField(label="Tell me about the incident.")
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5}
        ),
        label="Any comment or suggestion for that",
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message', ]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]
