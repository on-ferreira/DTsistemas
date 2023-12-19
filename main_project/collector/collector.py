import requests
from background_task import background
from datetime import timedelta, datetime
from logger import logger


@background(schedule=timedelta(seconds=15))
def run_communication_background(collector_dict):
    collector_instance = Collector(**collector_dict)
    collector_instance._run_communication()


URL_SYNTHESIS = "http://dtsistemas:5095/synthesis"


class Collector:
    def __init__(self, synthesis_url=f"{URL_SYNTHESIS}/get_active_projects",
                 communication_url=f"{URL_SYNTHESIS}/comunication_collector_synthesis/",
                 project_list=None):
        self.synthesis_url = synthesis_url
        self.communication_url = communication_url
        self.project_list = project_list or requests.get(self.synthesis_url).json()

    def _run_communication(self):
        logger.debug(f"Collector | _run_communication at {datetime.now()}")
        self._establish_connection_and_send_data()

    def _establish_connection_and_send_data(self):
        logger.debug(f"Collector | _establish_connection_and_send_data at {datetime.now()}")
        try:
            response = requests.get(self.communication_url)
            projects = response.json()
            logger.debug(f"Collector | Projects Received {projects}")
            collected_data = self._get_collected_data(projects)
            self._send_collected_data(collected_data)
        except requests.exceptions.RequestException as e:
            logger.debug(f"Collector | Error establishing connection with synthesis: {e}")

    def _get_collected_data(self, projects):
        collected_data = {}
        for project in projects:
            data_response = {}
            for tag in projects[project]["tags"]:
                tag_response = requests.get(projects[project]['link']).json()
                data_response[tag] = tag_response
            collected_data[project] = data_response
        return collected_data

    def _send_collected_data(self, collected_data):
        headers = {'Content-Type': 'application/json'}
        if collected_data:
            post_response = requests.post(self.communication_url, json=collected_data, headers=headers)
            logger.debug(f"Collector | Status Code: {post_response.status_code}")
        self.run_communication()

    def run_communication(self):
        # self._run_communication()
        logger.debug(f"Collector | run_communication at {datetime.now()}")
        collector_dict = self.to_dict()
        run_communication_background(collector_dict)

    def to_dict(self):
        """Return a dictionary representation of the instance"""
        return {
            "synthesis_url": self.synthesis_url,
            "communication_url": self.communication_url,
            "project_list": self.project_list
        }
