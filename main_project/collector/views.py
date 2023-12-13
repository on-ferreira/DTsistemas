from django.shortcuts import render
from django.http import HttpResponse
from logger import logger
from .collector import Collector, run_sem_class
from datetime import datetime

def collector_view(request):
    logger.debug(f"Collector | This is a debug message from Collector at {datetime.now()}")
    worker = Collector()
    worker.run_communication()
    return HttpResponse("You are in Collector")