##
#    Copyright (C) 2014 Jessica Tallon & Matt Molyneaux
#   
#    This file is part of Inboxen.
#
#    Inboxen is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Inboxen is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with Inboxen.  If not, see <http://www.gnu.org/licenses/>.
##

from django import test
from django.core import urlresolvers

from inboxen import models

@test.utils.override_settings(CELERY_ALWAYS_EAGER=True)
class HomeViewTestCase(test.TestCase):
    fixtures = ['inboxen_testdata.json']

    def setUp(self):
        self.user = models.User.objects.get(id=1)

        self.client = test.Client()
        login = self.client.login(username=self.user.username, password="123456")

        if not login:
            raise Exception("Could not log in")

    def get_url(self):
        return urlresolvers.reverse("user-home")

    def test_get(self):
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)

    def test_pagin(self):
        # there should be 150 inboxes in the test fixtures
        # and pages are paginated by 100 items
        response = self.client.get(self.get_url() + "2")
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.get_url() + "3")
        self.assertEqual(response.status_code, 404)
