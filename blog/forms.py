from django import forms

from .models import Post, Comment, Category


class GetForm(forms.ModelForm):
    title = forms.CharField(required=False)
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': "categories"}))

    class Meta:
        model = Post
        fields = ('title', 'categories')


class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': "categories"}))

    class Meta:
        model = Post
        fields = ('categories', 'title', 'text')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)
