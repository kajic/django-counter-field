from django.db import models


class CounterField(models.IntegerField):
    """
    CounterField wraps the standard django IntegerField. It exists primarily to allow for easy validation of
    counter fields. The default value of a counter field is 0.
    """

    def __init__(self, *args, **kwargs):
        kwargs["default"] = kwargs.get("default", 0)
        super().__init__(*args, **kwargs)
