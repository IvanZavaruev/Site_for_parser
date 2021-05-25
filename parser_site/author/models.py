from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=122)

    def __str__(self):
        return self.name


class Years(models.Model):
    year = models.IntegerField(max_length=20, primary_key=True, unique=True)

    def __str__(self):
        return self.year


class Publication(models.Model):
    title = models.CharField(max_length=540, unique=True)
    authors = models.ManyToManyField(Author)
    link = models.CharField(max_length=122, unique=True)
    info = models.CharField(max_length=540)
    year = models.ForeignKey(Years, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

