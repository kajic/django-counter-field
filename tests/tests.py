from django.test import TestCase

from .models import User, Relationship, Article


class RelationshipsTestCase(TestCase):
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


class CommentsTestCase(TestCase):
    def test_is_in_counter(self):
        user = User()
        user.save()

        article = Article(user=user)
        article.save()

        user = User.objects.get(pk=user.pk)

        self.assertEqual(user.draft_count, 1)
        self.assertEqual(user.published_count, 0)

        article = Article.objects.get(pk=article.pk)
        article.is_draft = False
        article.save()

        user = User.objects.get(pk=user.pk)

        self.assertEqual(user.draft_count, 0)
        self.assertEqual(user.published_count, 1)
