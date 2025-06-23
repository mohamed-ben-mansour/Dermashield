# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth.models import User
# from feedback.models import Feedback


# class FeedbackViewsTest(TestCase):
#     def setUp(self):
#         # Create user and log in
#         self.user = User.objects.create_user(username='testuser', password='12345')
#         self.client = Client()
#         self.client.login(username='testuser', password='12345')

#         # Create a feedback for tests
#         self.feedback = Feedback.objects.create(
#             user=self.user,
#             comment='Good feedback',
#             rating=4,
#             sentiment='positif'
#         )

#     def test_feedback_list_view(self):
#         url = reverse('feedback_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Good feedback')

#     def test_feedback_create_get(self):
#         url = reverse('feedback_create')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)

#     def test_feedback_create_post_valid(self):
#         url = reverse('feedback_create')
#         data = {
#             'comment': 'This is a nice comment',
#             'rating': 5,
#         }
#         response = self.client.post(url, data)
#         self.assertRedirects(response, reverse('all_feedbacks'))
#         self.assertTrue(Feedback.objects.filter(comment='This is a nice comment').exists())

#     def test_feedback_create_post_bad_word(self):
#         url = reverse('feedback_create')
#         data = {
#             'comment': 'This contains badword1',
#             'rating': 3,
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Votre commentaire contient des mots inappropriés.')

#     def test_feedback_create_post_empty_comment(self):
#         url = reverse('feedback_create')
#         data = {
#             'comment': '',
#             'rating': 3,
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Le commentaire ne peut pas être vide.')

#     def test_feedback_edit_get(self):
#         url = reverse('feedback_edit', args=[self.feedback.id])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Good feedback')

#     def test_feedback_edit_post(self):
#         url = reverse('feedback_edit', args=[self.feedback.id])
#         data = {
#             'comment': 'Updated comment',
#             'rating': 2,
#         }
#         response = self.client.post(url, data)
#         self.assertRedirects(response, reverse('all_feedbacks'))
#         self.feedback.refresh_from_db()
#         self.assertEqual(self.feedback.comment, 'Updated comment')

#     def test_feedback_delete_get(self):
#         url = reverse('feedback_delete', args=[self.feedback.id])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Good feedback')

#     def test_feedback_delete_post(self):
#         url = reverse('feedback_delete', args=[self.feedback.id])
#         response = self.client.post(url)
#         self.assertRedirects(response, reverse('all_feedbacks'))
#         self.assertFalse(Feedback.objects.filter(id=self.feedback.id).exists())

#     def test_all_feedbacks_view(self):
#         url = reverse('all_feedbacks')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Good feedback')

#     def test_feedback_statistics_view(self):
#         url = reverse('feedback_statistics')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'positif')

# feedback/tests/test_admin.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from feedback.models import Feedback

User = get_user_model()

class FeedbackAdminTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='user', password='user', is_staff=True, is_superuser=True
        )
        self.client.login(username='user', password='user')

    def test_add_feedback_via_admin(self):
        response = self.client.post('/admin/feedback/feedback/add/', {
            'user': self.admin_user.id,
            'comment': 'Great app 👍',
            'gif_url': 'https://example.com/test.gif',
            'sentiment': 'Neutre',
            'rating': 4,
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "was added successfully")
        self.assertTrue(Feedback.objects.filter(comment__icontains='Great').exists())

    # def test_edit_feedback_via_admin(self):
    #     feedback = Feedback.objects.create(
    #         user=self.admin_user,
    #         comment='Initial comment',
    #         sentiment='Neutre',
    #         rating=2
    #     )

    #     response = self.client.post(f'/admin/feedback/feedback/{feedback.id}/change/', {
    #         'user': self.admin_user.id,
    #         'comment': 'Updated comment',
    #         'gif_url': '',
    #         'sentiment': 'Neutre',
    #         'rating': 5,
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "was changed successfully")
    #     feedback.refresh_from_db()
    #     self.assertEqual(feedback.comment, 'Updated comment')

    # def test_delete_feedback_via_admin(self):
    #     feedback = Feedback.objects.create(
    #         user=self.admin_user,
    #         comment='Delete me',
    #         rating=1
    #     )

    #     response = self.client.post(f'/admin/feedback/feedback/{feedback.id}/delete/', {
    #         'post': 'yes'
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "was deleted successfully")
    #     self.assertFalse(Feedback.objects.filter(id=feedback.id).exists())
