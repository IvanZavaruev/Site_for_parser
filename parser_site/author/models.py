from django.db import models


class Author(models.Model):
    """A class used to create Authors table

    ...

    Attributes
    ----------
    name : str
        name of the author of the publication
    """
    name = models.CharField(max_length=122)

    def __str__(self):
        return self.name


class Years(models.Model):
    """A class used to create Years table

    ...

    Attributes
    ----------
    year : int
        year of printing publication
    """
    year = models.IntegerField(primary_key=True, unique=True)

    def __str__(self):
        return str(self.year)


class Publication(models.Model):
    """A class used to create Publication table

    ...

    Attributes
    ----------
    title : str
        title of publication
    authors:
        name of the author of the publication.
        This column is related to the Authors table
    link: str
        link to the publication site
    info: str
        all information about the publisher of the publication
    year :
        year of printing publication.
        This column is related to the Years table
    """
    title = models.CharField(max_length=540, unique=True)
    authors = models.ManyToManyField(Author)
    link = models.CharField(max_length=122, unique=True)
    info = models.CharField(max_length=540)
    year = models.ForeignKey(Years, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

