import tempfile
import csv
from pathlib import Path
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from elibrary_parser.Parsers import AuthorParser
from .models import Years


def index(request):
    return HttpResponse('Author working')


def save_publication_to_csv(tmpdir, author_id, response, parser):
    save_path = Path(f"{tmpdir}/processed/{str(author_id)}")
    save_path.mkdir(exist_ok=True)

    csv_path = save_path / "publications.csv"
    with open(csv_path, 'a', encoding="utf8", newline='') as csvfile:
        wr = csv.writer(response, csvfile, delimiter=';')
        for publication in parser.publications:
            saving_publication = [
                publication.title,
                publication.authors,
                publication.info,
                publication.link,
                publication.year
            ]
            wr.writerow(saving_publication)

    return response


def publication_json(parser):
    json_data = []
    for publication in parser.publications:
        saving_publication = (
            publication.title,
            publication.authors,
            publication.info,
            publication.link,
            publication.year
        )
        json_data.append(saving_publication)
    to_json = {"publications": json_data}

    return to_json


def publications(request, author_id):
    format = request.GET.get('format', None)

    year_from = request.GET.get('year_from', 2015)
    year_to = request.GET.get('year_to', 2021)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename= "{author_id}.csv"'

    try:
        int(year_from)
        int(year_to)
    except ValueError:
        year_from = 2015
        year_to = 2021

    with tempfile.TemporaryDirectory() as tmpdir:
        parser = AuthorParser(
            author_id=str(author_id),
            data_path=tmpdir,
            date_from=int(year_from),
            date_to=int(year_to))
        parser.find_publications()
        parser.parse_publications()
        add_years_to_Data_Base(parser, Years)
        if format == 'json':
            return JsonResponse(publication_json(parser))
        else:
            return save_publication_to_csv(tmpdir, author_id, response, parser)


def add_years_to_Data_Base(parser, Years):
    for publication in parser.publications:
        year_for_save = Years(year=publication.year)
        year_for_save.save()
