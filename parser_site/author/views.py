import tempfile
from django.shortcuts import render
from django.http import HttpResponse
from elibrary_parser.Parsers import AuthorParser


def index(request):
    return HttpResponse('Author working')


def publications(request, author_id):
    with tempfile.TemporaryDirectory() as tmpdir:
        parser = AuthorParser(author_id=author_id, data_path=tmpdir,date_from=2019, date_to=2021)
    parser.find_publications()
    parser.parse_publications()

    return HttpResponse(author_id.publications)
