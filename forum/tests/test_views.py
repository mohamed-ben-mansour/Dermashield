from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Forum, Comment, Response
from .forms import ForumForm, CommentForm, ResponseForm

class ForumViewsTest(TestCase):
    def setUp(self):
        # Create a user and login client
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client = Client()
        self.client.login(username='testuser', password='pass')

        # Create a forum instance
        self.forum = Forum.objects.create(title='Test Forum', content='Content', upvotes=0)

        # Create a comment instance linked to forum and user
        self.comment = Comment.objects.create(
            forum=self.forum,
            user=self.user,
            content='Test comment',
        )

        # Create a response instance linked to comment and user
        self.response = Response.objects.create(
            comment=self.comment,
            user=self.user,
            content='Test response',
        )

    def test_forum_list_view(self):
        url = reverse('forum:forum_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('page_obj', response.context)
        self.assertTemplateUsed(response, 'forum/forum_list.html')

    def test_forum_detail_get(self):
        url = reverse('forum:forum_details1', args=[self.forum.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['forum'], self.forum)
        self.assertTemplateUsed(response, 'forum/forum_details1.html')

    def test_forum_detail_post_add_comment(self):
        url = reverse('forum:forum_details1', args=[self.forum.id])
        data = {
            'content': 'A new comment without bad words',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, url)
        self.assertTrue(Comment.objects.filter(content='A new comment without bad words').exists())

    def test_forum_detail_post_inappropriate_word(self):
        url = reverse('forum:forum_details1', args=[self.forum.id])
        data = {
            'content': 'This contains mot1 which is inappropriate',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, url)
        self.assertFalse(Comment.objects.filter(content__contains='mot1').exists())

    def test_forum_create_get(self):
        url = reverse('forum:forum_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ForumForm)
        self.assertTemplateUsed(response, 'forum/forum_form.html')

    def test_forum_create_post_valid(self):
        url = reverse('forum:forum_create')
        data = {
            'title': 'Created Forum',
            'content': 'Forum content here',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('forum:forum_list'))
        self.assertTrue(Forum.objects.filter(title='Created Forum').exists())

    def test_forum_update_get(self):
        url = reverse('forum:forum_update', args=[self.forum.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ForumForm)
        self.assertTemplateUsed(response, 'forum/forum_form.html')

    def test_forum_update_post_valid(self):
        url = reverse('forum:forum_update', args=[self.forum.id])
        data = {
            'title': 'Updated Title',
            'content': 'Updated content',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('forum:forum_list'))
        self.forum.refresh_from_db()
        self.assertEqual(self.forum.title, 'Updated Title')

    def test_forum_delete_get(self):
        url = reverse('forum:forum_delete', args=[self.forum.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/forum_confirm_delete.html')

    def test_forum_delete_post(self):
        url = reverse('forum:forum_delete', args=[self.forum.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('forum:forum_list'))
        self.assertFalse(Forum.objects.filter(id=self.forum.id).exists())

    def test_upvote_forum(self):
        url = reverse('forum:upvote_forum', args=[self.forum.id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('forum:forum_list'))
        self.forum.refresh_from_db()
        self.assertEqual(self.forum.upvotes, 1)

    def test_delete_comment_get_not_author_redirect(self):
        # Create another user to test access denial
        other_user = User.objects.create_user(username='otheruser', password='pass')
        self.client.logout()
        self.client.login(username='otheruser', password='pass')

        url = reverse('forum:onfirm_delete_comment', args=[self.comment.id])
        response = self.client.get(url)
        # Should redirect because user is not author
        self.assertRedirects(response, reverse('forum:forum_details1', args=[self.forum.id]))

    def test_delete_comment_post(self):
        url = reverse('forum:onfirm_delete_comment', args=[self.comment.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('forum:forum_details1', args=[self.forum.id]))
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_reply_to_comment_get(self):
        url = reverse('forum:reply_to_comment', args=[self.comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ResponseForm)
        self.assertTemplateUsed(response, 'forum/reply_to_comment.html')

    def test_reply_to_comment_post_valid(self):
        url = reverse('forum:reply_to_comment', args=[self.comment.id])
        data = {'content': 'A reply'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('forum:forum_details1', args=[self.forum.id]))
        self.assertTrue(Response.objects.filter(content='A reply').exists())

    def test_delete_response(self):
        url = reverse('forum:delete_response', args=[self.response.id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('forum:forum_details1', args=[self.forum.id]))
        self.assertFalse(Response.objects.filter(id=self.response.id).exists())
