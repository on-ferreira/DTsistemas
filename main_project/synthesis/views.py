from django.shortcuts import render
from django.http import HttpResponse
from logger import logger

def synthesis_view(request):
    logger.debug("Synthesis | This is a debug message from Synthesis")
    return HttpResponse("You are in Synthesis")