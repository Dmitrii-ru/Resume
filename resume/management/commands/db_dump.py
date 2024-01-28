import os
from django.core.management import call_command
from resume.management.base_commends.base_db_dump import BaseDumpDB


class Command(BaseDumpDB):
    help = 'Dump data base'

    def dump_data(self):
        path = os.path.join(self.get_path_dump_dir(), self.dump_file_name)
        try:
            with open(path, 'w') as file:
                call_command('dumpdata', stdout=file)
            message = 'Резервная копия успешно сохранена'
            self.stdout.write(self.style.SUCCESS(message))

        except Exception as e:
            message = f'Не возможно создать резервную копию:: {str(e)}'
            self.stderr.write(self.style.ERROR(message))

    def handle(self, *args, **options):
        self.dump_data()
