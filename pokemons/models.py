from django.db import models

# Create your models here.


def get_default_something():
    return []


class Pokemon(models.Model):
    # 為了方便測試，number 不加 unique key
    number = models.TextField()
    name = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    types = models.JSONField(default=get_default_something)

    # types = models.ManyToManyField(Type)

    def __str__(self):
        return str(self.__dict__)

    class Meta:
        ordering = ['-created_at']
