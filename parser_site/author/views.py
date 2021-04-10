import tempfile
from django.shortcuts import render
from django.http import HttpResponse
from elibrary_parser.Parsers import AuthorParser


def index(request):
    return HttpResponse('Author working')


def publications(request, author_id):
    year_from = request.GET.get('year_from', 2015)
    year_to = request.GET.get('year_to', 2021)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= author_id + ".csv"'
    with tempfile.TemporaryDirectory() as tmpdir:
        parser = AuthorParser(author_id=str(author_id), data_path=tmpdir, date_from=int(year_from), date_to=int(year_to))
        parser.find_publications()
        parser.parse_publications()
        parser.save_publications(response)

    return response
