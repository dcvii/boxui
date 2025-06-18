from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from wagtail.models import Page


class Comment(models.Model):
    """Model for comments on article pages"""
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    karma_score = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.page.title}"
    
    def update_karma_score(self):
        """Calculate and update karma score based on interactions"""
        total_karma = self.interactions.aggregate(
            total=Sum('reaction')
        )['total'] or 0
        self.karma_score = total_karma
        self.save(update_fields=['karma_score'])


class CommentInteraction(models.Model):
    """Model for user interactions (upvotes/downvotes) with comments"""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='interactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.IntegerField(choices=[(1, 'Upvote'), (-1, 'Downvote')])
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('comment', 'user')  # One vote per user per comment
    
    def __str__(self):
        reaction_str = "upvoted" if self.reaction > 0 else "downvoted"
        return f"{self.user.username} {reaction_str} comment {self.comment.id}"
    
    def save(self, *args, **kwargs):
        """Override save to update comment karma when interaction is saved"""
        super().save(*args, **kwargs)
        self.comment.update_karma_score()
    
    def delete(self, *args, **kwargs):
        """Override delete to update comment karma when interaction is deleted"""
        comment = self.comment
        super().delete(*args, **kwargs)
        comment.update_karma_score()

