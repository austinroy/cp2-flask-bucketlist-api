import unittest

import config
from app import db, app
from app.auth.models import User
from app.bucketlists.models import BucketList, BucketListItem


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """Sets up sample data for the tests"""
        app.testing = True
        self.client = app.test_client(use_cookies=False)

        config.SQLALCHEMY_DATABASE_URI = 'sqlite://'
        app.config.from_object(config)
        db.create_all()

        # Create sample users for tests
        self.austin = User('austin', 'password')
        self.austin.save()
        self.austin.refresh_from_db()

        self.roy = User('roy', 'password')
        self.roy.save()
        self.roy.refresh_from_db()

        # Create sample bucket lists for each user
        self.austin_bucketlist = BucketList("Checkpoint 2", self.austin.id)
        self.austin_bucketlist.save()
        self.austin_bucketlist.refresh_from_db()

        self.roy_bucketlist = BucketList("Checkpoint ", self.roy.id)
        self.roy_bucketlist.save()
        self.roy_bucketlist.refresh_from_db()

        # Add item  to bucket list
        name = "Learn more django"
        description = "Learn some JS"
        bucketlist_id = self.austin_bucketlist.id
        done = False
        self.austin_bucketlist_item = BucketListItem(
            name, description, bucketlist_id, done)
        self.austin_bucketlist_item.save()
        self.austin_bucketlist_item.refresh_from_db()

        db.session.commit()

        self.token = {'Authorization': 'Token ' + self.austin.token.decode(),
                      'Content-Type': 'application/json'}
        self.expired_token = {'Authorization': 'Token {}'.format(
            'austin.C2dRGQ.5bEgRGpUpHnxUDfS7WMB6crzlLA'),
            'Content-Type': 'application/json'}
        self.invalid_token = {'Authorization': 'Token abc',
                              'Content-Type': 'application/json'}

    def tearDown(self):
        """Clears data upon test completion"""
        db.session.remove()
        db.drop_all()
