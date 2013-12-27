from django.db import models

from django_counter_field import CounterField, CounterMixin, connect_counter


class User(models.Model):
    name = models.CharField(max_length=100)
    following_count = CounterField()
    followers_count = CounterField()
    published_count = CounterField()
    draft_count = CounterField()


class Relationship(CounterMixin, models.Model):
    consumer = models.ForeignKey('User', related_name='producer_set')
    producer = models.ForeignKey('User', related_name='consumer_set')

connect_counter('following_count', Relationship.consumer)
connect_counter('followers_count', Relationship.producer)


class Article(CounterMixin, models.Model):
    user = models.ForeignKey('User')
    is_draft = models.BooleanField(default=True)

connect_counter('published_count', Article.user, lambda article: not article.is_draft)
connect_counter('draft_count', Article.user, lambda article: article.is_draft)