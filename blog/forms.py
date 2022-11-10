from django import forms

from .models import Post, Comment, Category


class GetForm(forms.ModelForm):
    title = forms.CharField(required=False)
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Post
        fields = ('title', 'category')


class PostForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Post
        fields = ('category', 'title', 'text')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)
