from django.shortcuts import render
from django.http import HttpResponse
from logger import logger

def collector_view(request):
    logger.debug("Collector | This is a debug message from Collector")
    return HttpResponse("You are in Collector")