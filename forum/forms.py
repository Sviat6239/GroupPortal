from django import forms
from .models import Category, Tag, Forum, Thread, Comment, Poll, PollOption, UserProfile, Achievement

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter category name'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Optional description'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(name__iexact=name).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError("A category with this name already exists.")
        return name

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter tag name'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Tag.objects.filter(name__iexact=name).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError("A tag with this name already exists.")
        return name

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['name', 'description', 'categories', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter forum name'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the forum'}),
            'categories': forms.CheckboxSelectMultiple,
            'tags': forms.CheckboxSelectMultiple,
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Forum.objects.filter(name__iexact=name).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError("A forum with this name already exists.")
        return name

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'description', 'category', 'tags', 'status', 'attachment']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter thread title'}),
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Write your thread content'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.CheckboxSelectMultiple,
            'status': forms.Select(choices=Thread.STATUS_CHOICES),
            'attachment': forms.FileInput(attrs={'accept': '.pdf,.jpg,.png,.doc,.docx'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        if not (title and description):
            raise forms.ValidationError("Both title and description are required.")
        return cleaned_data

class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Comment
        fields = ['content', 'attachment']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment'}),
            'attachment': forms.FileInput(attrs={'accept': '.pdf,.jpg,.png,.doc,.docx'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("Comment content is required.")
        return cleaned_data

class PollForm(forms.ModelForm):
    options = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter one option per line'}),
        help_text="Enter at least two options, one per line."
    )

    class Meta:
        model = Poll
        fields = ['question']
        widgets = {
            'question': forms.TextInput(attrs={'placeholder': 'Enter poll question'}),
        }

    def clean_options(self):
        options = self.cleaned_data['options'].strip().split('\n')
        options = [opt.strip() for opt in options if opt.strip()]
        if len(options) < 2:
            raise forms.ValidationError("At least two options are required.")
        return options

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'location', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself'}),
            'avatar': forms.FileInput(attrs={'accept': '.jpg,.png,.gif'}),
            'location': forms.TextInput(attrs={'placeholder': 'Your location'}),
            'website': forms.URLInput(attrs={'placeholder': 'Your website'}),
        }

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['name', 'description', 'badge_image', 'points']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Achievement name'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the achievement'}),
            'badge_image': forms.FileInput(attrs={'accept': '.jpg,.png'}),
            'points': forms.NumberInput(attrs={'min': 0}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Achievement.objects.filter(name__iexact=name).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError("An achievement with this name already exists.")
        return name