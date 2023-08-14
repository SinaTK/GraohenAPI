from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return '{}, {} years old.'.format(self.name, self.age)

class Car(models.Model):
    owner = models.ManyToManyField(Person)
    model = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return '{}-{}, belong to {}'.format(self.model, self.year, self.owner.name)

