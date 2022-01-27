from django.test import TestCase


class MainpageTests(TestCase):
    #является ли post_list.html результатом запроса по /
    def test_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'blog/post_list.html')
