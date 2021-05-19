from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=122)


class Years(models.Model):
    years = models.CharField(max_length=20)


class Publication(models.Model):
    title = models.CharField(max_length=500)
    authors = models.ManyToManyField(Author)
    info = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    year = models.ForeignKey(Years, on_delete=models.CASCADE())
# Создать класс Автор с соответствующими атрибутами (название, авторы, инфо, ссылки, год )?
# в урлах ссылка на id автора, а views функция для парсинга
