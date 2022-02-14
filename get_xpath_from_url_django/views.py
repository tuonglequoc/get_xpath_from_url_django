from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import json

from . import helpers

@api_view(['POST', 'GET'])
def get_xpath(request):
    if request.method == 'GET':
        return render(request, 'get_xpath.html')
    elif request.method == 'POST':
        url = request.POST.get("url")
        content = helpers.get_data_from_url_by_chromedriver(url)
        soup = helpers.get_bs_data(content)
        xpath_data = helpers.get_xpath(soup)
        title = helpers.get_title(soup)
        return HttpResponse(json.dumps({"title": title, "xpaths": xpath_data}, indent=4))