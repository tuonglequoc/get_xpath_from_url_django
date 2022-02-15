from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view
from selenium.common.exceptions import InvalidArgumentException
import json

from . import helpers

@api_view(['POST'])
def get_xpath(request):
    url = json.loads(request.body).get("url")
    if not url:
        return HttpResponseBadRequest("Data body is invalid!")
    try:
        content = helpers.get_data_from_url_by_chromedriver(url)
    except InvalidArgumentException:
        return HttpResponseBadRequest("URL is invalid!")
    soup = helpers.get_bs_data(content)
    xpath_data = helpers.get_xpath(soup)
    title = helpers.get_title(soup)
    return HttpResponse(json.dumps({"title": title, "xpaths": xpath_data}, indent=4))