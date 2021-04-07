from django.db import models


class Publication(models.Model):
    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=500)
    info = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    year = models.CharField(max_length=500)
# Создать класс Автор с соответствующими атрибутами (название, авторы, инфо, ссылки, год )?
# в урлах ссылка на id автора, а views функция для парсинга
