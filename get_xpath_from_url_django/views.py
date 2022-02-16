from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view
from selenium.common.exceptions import InvalidArgumentException
import json

from . import helpers

# accept only POST request
@api_view(['POST'])
def get_xpath(request):
    # parse body data to dict and get the url
    url = json.loads(request.body).get("url")

    # data invalid exception
    if not url:
        return HttpResponseBadRequest("Data body is invalid!")

    # get html plain using chromedriver
    try:
        content = helpers.get_data_from_url_by_chromedriver(url)
    except InvalidArgumentException:
        # catch invalid url exception
        return HttpResponseBadRequest("URL is invalid!")

    # convert plain html to BeautifulSoup
    soup = helpers.get_bs_data(content)

    # get xpaths
    xpath_data = helpers.get_xpath(soup)

    # get title
    title = helpers.get_title(soup)

    # success and response to the client
    return HttpResponse(json.dumps({"title": title, "xpaths": xpath_data}, indent=4))