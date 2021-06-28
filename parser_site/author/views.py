import tempfile
import csv
import pandas
from pathlib import Path
from django.urls import reverse
from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from elibrary_parser.Parsers import AuthorParser


def index(request):
    """loads and shows main page of Parser web-site

    Parameters
    ----------
    request
        a standart Django parameter in views.py that
        contains data about the request

    Returns
    -------
    Html-page
    """
    template = loader.get_template('author/index.html')

    return HttpResponse(template.render())


def search(request):
    """takes author_id from the form html page and
       pass it to URL int:author_id/publications/

    Parameters
    ----------
    request
        a standart Django parameter in views.py that
        contains data about the request

    Returns
    -------
    redirects to URL int:author_id/publications/
    """
    if request.method == 'GET':
        author_id = request.GET['author_id']
        return HttpResponseRedirect(reverse('publications', args=[author_id]))


def save_publication_to_csv_or_xlsx(tmpdir, author_id, parser, format):
    """Return list of publications in csv or xlsx format

    Parameters
    ----------
    tmpdir : str
        path to temp directory
    author_id : int
        unique author number from the Elibrary.ru
    parser:
        object of class AuthorParser
    format:
        get request parameter

    Returns
    -------
    csv-file or xlsx-file
    """
    save_path = Path(f"{tmpdir}/processed/{str(author_id)}")
    save_path.mkdir(exist_ok=True)

    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename= "{author_id}.csv"'

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
    else:
        dict_for_excel = ({'Заголовок публикации': [],
                           'Авторы публикации': [],
                           'Библиографическая информация': [],
                           'Ссылка на Elibrary.ru': [],
                           'Год публикации': []})
        for publication in parser.publications:
            dict_for_excel['Заголовок публикации'].append(publication.title)
            dict_for_excel['Авторы публикации'].append(publication.authors)
            dict_for_excel['Библиографическая информация'].append(publication.info)
            dict_for_excel['Ссылка на Elibrary.ru'].append(publication.link)
            dict_for_excel['Год публикации'].append(int(publication.year))
        excel = pandas.DataFrame(dict_for_excel)
        excel.to_excel(f'{save_path}/{author_id}.xlsx', index=False)
        with open(f'{save_path}/{author_id}.xlsx', 'rb') as file_fo_download:
            response = HttpResponse(file_fo_download.read())
            response['Content-Disposition'] = f'attachment; filename={author_id}.xlsx'
            response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    return response


def publication_json(parser):
    """Return list of publication in json format

    Parameter
    ---------
    parser:
        object of class AuthorParser

    Returns
    -------
    Dict with 'publications' key """
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
    """Parses publications using AuthorParser
    this method can take data output format,
    define search range by publication year
    (year_from and year_to - start and end of range)

    Parameters
    ----------
    request:
        a standart Django parameter in views.py that
        contains data about the request
    author_id: int
        unique author number from the Elibrary.ru

    Returns
    -------
    list of publication in csv, xlsx, json format
    """
    format = request.GET.get('format', None)
    print(type(format))
    year_from = request.GET.get('year_from', 2015)
    year_to = request.GET.get('year_to', 2021)

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
        if format != 'json':
            return save_publication_to_csv_or_xlsx(tmpdir, author_id, parser, format)
        else:
            return JsonResponse(publication_json(parser))
