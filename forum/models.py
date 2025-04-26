from django.db import models
from authentification.models import CustomUser

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class Achievement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    badge_image = models.ImageField(upload_to='badges/', null=True, blank=True)
    points = models.PositiveIntegerField(default=0)
    criteria = models.CharField(max_length = 255)

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Forum(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='forums')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, blank=True, related_name='forums')
    tags = models.ManyToManyField(Tag, blank=True, related_name='forums')

    def __str__(self):
        return self.name

# ----- Threads -----

class Thread(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('moderation', 'Under Moderation'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='threads')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='threads')
    tags = models.ManyToManyField(Tag, blank=True, related_name='threads')
    views = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class ThreadSubscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'thread')

class SavedThread(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'thread')

class ThreadEditHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    old_content = models.TextField()
    new_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

class ThreadVote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=[('up', 'Upvote'), ('down', 'Downvote')])
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'thread')

# ----- Polls -----

class Poll(models.Model):
    thread = models.OneToOneField(Thread, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)

class PollVote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'option')

# ----- Comments -----

class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.thread.title}"

class CommentEditHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    old_content = models.TextField()
    new_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

class CommentVote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=[('up', 'Upvote'), ('down', 'Downvote')])
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')
