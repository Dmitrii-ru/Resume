import os

from django.apps import apps
from django.core.management.base import BaseCommand


class BaseDumpDB(BaseCommand):
    dump_file_name = 'resume_db_dump.json'
    @staticmethod
    def get_path_dump_dir():
        """
        Get or make dir
        """
        app_path = apps.get_app_config('resume').path
        dump_dir = os.path.join(app_path, 'utils/dump/')
        if not os.path.exists(dump_dir):
            os.makedirs(dump_dir)
        return dump_dir
