from django.shortcuts import render

from django.http import HttpResponse
from django.http import JsonResponse

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from logger import logger

from .models import Project
from .models import ProjectTag
from .models import Tag

from .DAO import get_all_projects
from .DAO import get_oldest_value_for_project_and_tag
from .DAO import get_recent_value_for_project_and_tag
from .DAO import get_all_tags
from .DAO import get_project_by_id
from .DAO import get_tag_by_id

import json
import concurrent.futures
import time

from datetime import datetime
from datetime import timedelta
from datetime import timezone

def synthesis_view(request):
    logger.debug("Synthesis | This is a debug message from Synthesis")
    return HttpResponse("You are in Synthesis")

@require_http_methods(["GET"])
def get_active_projects(request):
    projects = get_all_projects()
    project_dict = {project.id: {
        'name': project.name,
        'poco': project.poco,
        'um': project.um,
        'link': project.link
    } for project in projects}

    return JsonResponse(project_dict, status=200)


# Check for an alternative to this decorator, as it reduces security
@csrf_exempt
@require_http_methods(["GET", "POST"])
def comunication_harverster_synthesis(request):
    if request.method == "GET":
        # Query the database for data that needs updating
        update_list = {}
        projects = get_all_projects()
        tags = get_all_tags()
        for project in projects:
            project_update = {}
            for tag in tags:
                latest_row = get_recent_value_for_project_and_tag(project.id, tag.tag_id)
                latest_time = latest_row.timestamp if latest_row else None

                if latest_time is None or latest_time < (datetime.now(timezone.utc) - timedelta(seconds=30)):
                    project_update[tag.tag_id] = {
                        "tag_lastime": latest_time
                    }

            update_list[project.id] = {
                "tags": project_update,
                "link": project.link
            }

        return JsonResponse(update_list, status=200)

    elif request.method == "POST":
        # Get data from the request body
        data = json.loads(request.body.decode("utf-8"))
        """
        The data is returning in the format:
            { 1(project_id) : { 1(tag_id) : json_response_from_url,
                                2(tag_id) : json_response_from_url2}
            } 
        """

        # Save the data to the database
        for (key, inner_data) in data.items():
            for (inner_key, tag_data) in inner_data.items():
                tag_id = inner_key
                save_value = ""
                try:
                    if tag_id == '1':
                        save_value = tag_data["value"]
                    elif tag_id == '2':
                        save_value = tag_data["data"][0]
                    elif tag_id == '3':
                        save_value = tag_data["results"][0]["question"]
                except:
                    logger.debug(f"Synthesis | Error saving tag: {tag_id}")
                actual_project = get_project_by_id(key)
                actual_tag = get_tag_by_id(tag_id)
                if save_value:
                    temp = ProjectTag(projeto=actual_project, tag=actual_tag, value=save_value)
                    temp.save()
                    logger.debug(f"Synthesis | Project ID: {key}, tag id: {tag_id} value: {save_value}")

        # purge_old_data()
        return JsonResponse({}, status=200)


# 1200 seconds = 20 minutes
def purge_old_data_for_project(project, keep_data_interval=1200):
    try:
        latest_row = ProjectTag.objects.filter(project_id=project.id).aggregate(Max('timestamp'))
        latest_time = latest_row['timestamp__max']
    except ProjectTag.DoesNotExist:
        latest_time = None
    for row in ProjectTag.objects.all():
        if latest_time and (row.timestamp < latest_time - keep_data_interval):
            if (row.project_id == project.id):
                row.delete()


def purge_old_data():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(purge_old_data_for_project, project) for project in get_all_projects()]
        concurrent.futures.wait(futures)
