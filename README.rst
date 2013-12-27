====================
django-counter-field
====================

It is sometimes useful to cache the total number of objects associated with another object through a ForeignKey
relation. For example the total number of comments associated with an article.

django-counter-field makes it easy to denormalize and keep such counters up to date.

Quick start
-----------

1. Install django-counter-field::

    pip install django-counter-field

2. Add "django_counter_field" to your INSTALLED_APPS setting::

    INSTALLED_APPS = (
        ...
        'django_counter_field',
    )

3. Add a CounterField to your model::

    from django_counter_field import CounterField


    class Article(models.Model):
        comment_count = CounterField()

4. Add the CounterMixin to the related model::

    from django_counter_field import CounterMixin, connect_counter


    class Comment(CounterMixin, models.Model):
        article = models.ForeignKey(Article)

5. Connect the related foreign key field with the counter field::

    connect_counter('comment_count', Comment.article)

Whenever a comment is created the comment_count on the associated Article will be incremented. If the comment is
deleted, the comment_count will be automatically decremented.


Overview
--------

Creating a new counter requires three simple steps:

1. Add a `CounterField` field to the parent model.
2. Add the `CounterMixin` mixin to the child model.
3. Use `connect_counter` to connect the child model with the new counter.

Most counters are simple in the sense that you want to count all child objects. Sometimes, however, objects should be
counted based on one or several conditions. For example you may not wish to count *all* comments on an article but
only comments that have been approved. You can create conditional counters by providing a third `is_in_counter_func`
argument to `connect_counter`:

    connect_counter('comment_count', Comment.article, lambda comment: comment.is_approved)

The `is_in_counter_func` function will be called with `Comment` objects and must return `True` if the given comment
should be counted. It must not concern itself with checking if the comment is deleted or not, django-counter-field
does that by default.

Backfilling
-----------

Often you will add a `CounterField` to a model that already has a large number of associated objects. When a counter
is created, it's value is initialized to zero. This value is likely incorrect. django-counter-field provides a couple
of management commands that allow you to rebuild the value of a counter:

1. List all available counters:

    $ python manage.py list_counters

2. Rebuild a counter using one of the counter names given by `list_counters`:

    $ python manage.py rebuild_counter <counter_name>

Note: The `rebuild_counter` management command will only update counters on objects that have at least one child
object. For example articles with at least one comment. Articles with no comments  will not be updated. This
is a conscious limitation; the use cases for such a feature seem very limited, if existent at all.


Documentation
-------------

    $ pip install Sphinx
    $ cd docs
    $ make html
    Open build/html/index.html
