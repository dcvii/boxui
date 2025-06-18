from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
import json

from home.models import ArticlePage
from .models import Comment, CommentInteraction
from wagtail.models import Page, Site


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create a root page and article page
        root_page = Page.objects.get(id=1)  # Wagtail creates a default root page
        self.article_page = ArticlePage(
            title='Test Article',
            body='<p>This is a test article</p>'
        )
        root_page.add_child(instance=self.article_page)
        
        self.comment = Comment.objects.create(
            page=self.article_page,
            user=self.user,
            text='This is a test comment'
        )

    def test_comment_creation(self):
        """Test that comments are created properly"""
        self.assertEqual(self.comment.text, 'This is a test comment')
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.page, self.article_page)
        self.assertEqual(self.comment.karma_score, 0)

    def test_comment_string_representation(self):
        """Test the string representation of comments"""
        expected = f"Comment by {self.user.username} on {self.article_page.title}"
        self.assertEqual(str(self.comment), expected)

    def test_karma_score_update(self):
        """Test that karma score updates correctly"""
        # Create upvote
        CommentInteraction.objects.create(
            comment=self.comment,
            user=self.user,
            reaction=1
        )
        
        # Karma should now be 1
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.karma_score, 1)

    def test_multiple_interactions(self):
        """Test karma calculation with multiple interactions"""
        user2 = User.objects.create_user(username='user2', password='pass')
        user3 = User.objects.create_user(username='user3', password='pass')
        
        # User 1 upvotes
        CommentInteraction.objects.create(
            comment=self.comment,
            user=self.user,
            reaction=1
        )
        
        # User 2 upvotes
        CommentInteraction.objects.create(
            comment=self.comment,
            user=user2,
            reaction=1
        )
        
        # User 3 downvotes
        CommentInteraction.objects.create(
            comment=self.comment,
            user=user3,
            reaction=-1
        )
        
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.karma_score, 1)  # 1 + 1 - 1 = 1


class CommentInteractionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        root_page = Page.objects.get(id=1)
        self.article_page = ArticlePage(
            title='Test Article',
            body='<p>Test content</p>'
        )
        root_page.add_child(instance=self.article_page)
        
        self.comment = Comment.objects.create(
            page=self.article_page,
            user=self.user,
            text='Test comment'
        )

    def test_interaction_creation(self):
        """Test that interactions are created properly"""
        interaction = CommentInteraction.objects.create(
            comment=self.comment,
            user=self.user,
            reaction=1
        )
        
        self.assertEqual(interaction.comment, self.comment)
        self.assertEqual(interaction.user, self.user)
        self.assertEqual(interaction.reaction, 1)

    def test_unique_constraint(self):
        """Test that one user can only have one interaction per comment"""
        CommentInteraction.objects.create(
            comment=self.comment,
            user=self.user,
            reaction=1
        )
        
        # Trying to create another interaction should fail
        with self.assertRaises(Exception):
            CommentInteraction.objects.create(
                comment=self.comment,
                user=self.user,
                reaction=-1
            )

    def test_interaction_string_representation(self):
        """Test string representation of interactions"""
        interaction = CommentInteraction.objects.create(
            comment=self.comment,
            user=self.user,
            reaction=1
        )
        
        expected = f"{self.user.username} upvoted comment {self.comment.id}"
        self.assertEqual(str(interaction), expected)

    def test_karma_update_on_interaction_save(self):
        """Test that karma is updated when interaction is saved"""
        initial_karma = self.comment.karma_score
        
        CommentInteraction.objects.create(
            comment=self.comment,
            user=self.user,
            reaction=1
        )
        
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.karma_score, initial_karma + 1)

    def test_karma_update_on_interaction_delete(self):
        """Test that karma is updated when interaction is deleted"""
        interaction = CommentInteraction.objects.create(
            comment=self.comment,
            user=self.user,
            reaction=1
        )
        
        # Karma should be 1
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.karma_score, 1)
        
        # Delete interaction
        interaction.delete()
        
        # Karma should be back to 0
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.karma_score, 0)


class KarmaAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        root_page = Page.objects.get(id=1)
        self.article_page = ArticlePage(
            title='Test Article',
            body='<p>Test content</p>'
        )
        root_page.add_child(instance=self.article_page)
        
        self.comment = Comment.objects.create(
            page=self.article_page,
            user=self.user,
            text='Test comment'
        )

    def test_karma_interaction_requires_login(self):
        """Test that karma interaction requires authentication"""
        response = self.client.post(
            reverse('comments:karma_interaction'),
            data=json.dumps({
                'comment_id': self.comment.id,
                'reaction': 1
            }),
            content_type='application/json'
        )
        
        # Should redirect to login or return 401/403
        self.assertIn(response.status_code, [302, 401, 403])

    def test_karma_interaction_upvote(self):
        """Test upvoting a comment"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('comments:karma_interaction'),
            data=json.dumps({
                'comment_id': self.comment.id,
                'reaction': 1
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['karma_score'], 1)
        self.assertEqual(data['user_reaction'], 1)

    def test_karma_interaction_downvote(self):
        """Test downvoting a comment"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('comments:karma_interaction'),
            data=json.dumps({
                'comment_id': self.comment.id,
                'reaction': -1
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['karma_score'], -1)
        self.assertEqual(data['user_reaction'], -1)

    def test_karma_interaction_toggle(self):
        """Test toggling a vote (voting same reaction twice)"""
        self.client.login(username='testuser', password='testpass123')
        
        # First vote
        response = self.client.post(
            reverse('comments:karma_interaction'),
            data=json.dumps({
                'comment_id': self.comment.id,
                'reaction': 1
            }),
            content_type='application/json'
        )
        
        data = json.loads(response.content)
        self.assertEqual(data['karma_score'], 1)
        
        # Vote again (toggle off)
        response = self.client.post(
            reverse('comments:karma_interaction'),
            data=json.dumps({
                'comment_id': self.comment.id,
                'reaction': 1
            }),
            content_type='application/json'
        )
        
        data = json.loads(response.content)
        self.assertEqual(data['karma_score'], 0)
        self.assertIsNone(data['user_reaction'])

    def test_get_comment_karma(self):
        """Test getting current karma for a comment"""
        response = self.client.get(
            reverse('comments:get_comment_karma', args=[self.comment.id])
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(data['karma_score'], 0)
        self.assertIsNone(data['user_reaction'])

    def test_invalid_comment_id(self):
        """Test handling of invalid comment ID"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('comments:karma_interaction'),
            data=json.dumps({
                'comment_id': 99999,
                'reaction': 1
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)

    def test_invalid_reaction_value(self):
        """Test handling of invalid reaction value"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('comments:karma_interaction'),
            data=json.dumps({
                'comment_id': self.comment.id,
                'reaction': 5  # Invalid reaction
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)

