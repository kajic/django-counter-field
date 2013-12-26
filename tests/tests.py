from django.test import TestCase

from .models import User, Relationship


class DjangoCounterTestCase(TestCase):
    def test_increment_decrement(self):
        me = User()
        me.save()
        you = User()
        you.save()

        self.assertEqual(me.following_count, 0)
        self.assertEqual(you.followers_count, 0)

        i_follow_you = Relationship(consumer=me, producer=you)
        i_follow_you.save()

        you_follow_me = Relationship(consumer=you, producer=me)
        you_follow_me.save()

        me = User.objects.get(pk=me.pk)
        you = User.objects.get(pk=you.pk)

        self.assertEqual(me.following_count, 1) # i follow you
        self.assertEqual(me.followers_count, 1) # you follow me
        self.assertEqual(you.following_count, 1) # you follow me
        self.assertEqual(you.followers_count, 1) # i follow you

        i_follow_you.delete()

        me = User.objects.get(pk=me.pk)
        you = User.objects.get(pk=you.pk)

        self.assertEqual(me.following_count, 0)
        self.assertEqual(me.followers_count, 1) # you follow me
        self.assertEqual(you.following_count, 1) # you follow me
        self.assertEqual(you.followers_count, 0)
