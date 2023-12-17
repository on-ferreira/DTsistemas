import requests
from background_task import background
from datetime import timedelta, datetime
from logger import logger


@background(schedule=timedelta(seconds=15))
def run_communication_background(collector_dict):
    collector_instance = Collector(**collector_dict)
    collector_instance._run_communication()


URL_SYNTHESIS = "5095/synthesis"


class Collector:
    def __init__(self, synthesis_url=f"http://localhost:{URL_SYNTHESIS}/get_active_projects",
                 communication_url=f"http://localhost:{URL_SYNTHESIS}/comunication_harverster_synthesis/",
                 project_list=None):
        self.synthesis_url = synthesis_url
        self.communication_url = communication_url
        self.project_list = project_list or []

    def _run_communication(self):
        logger.debug(f"Collector | _run_communication at {datetime.now()}")
        self._establish_connection_and_send_data()

    def _establish_connection_and_send_data(self):
        logger.debug(f"Collector | _establish_connection_and_send_data at {datetime.now()}"
                     f"\nActive projects: {self.project_list}")
        try:
            response = requests.get(self.synthesis_url)
            projects = response.json()
            harvested_data = self._get_harvested_data(projects)
            self._send_harvested_data(harvested_data)
        except requests.exceptions.RequestException as e:
            logger.debug(f"Collector | Error establishing connection with synthesis: {e}")

    def _get_harvested_data(self, projects):
        harvested_data = {}
        for project in projects:
            data_response = {}
            for tag in projects[project]["tags"]:
                tag_response = requests.get(self.tags_urls[tag]).json()
                data_response[tag] = tag_response
            harvested_data[project] = data_response
        return harvested_data

    def _send_harvested_data(self, harvested_data):
        headers = {'Content-Type': 'application/json'}
        if harvested_data:
            post_response = requests.post(self.communication_url, json=harvested_data, headers=headers)
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
