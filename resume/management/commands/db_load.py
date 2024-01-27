import os
from django.core.management import call_command
from resume.management.base_commends.base_db_dump import BaseDumpDB


class Command(BaseDumpDB):
    help = 'Load data base'

    def load_data(self):
        try:
            call_command('loaddata', os.path.join(self.get_path_dump_dir(), self.dump_file_name))
            message = 'База данных загружена'
            self.stdout.write(self.style.SUCCESS(message))
        except Exception as e:
            message = f'Не возможно загрузить базу данных: {str(e)}'
            self.stderr.write(self.style.ERROR(message))

    def handle(self, *args, **options):
        self.load_data()
