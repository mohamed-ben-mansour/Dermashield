import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gl_version1.settings')
django.setup()

with open('data.json', 'w', encoding='utf-8') as f:
    call_command(
        'dumpdata',
        natural_primary=True,
        natural_foreign=True,
        exclude=['auth.permission', 'contenttypes'],
        stdout=f,
        indent=2
    )

print("Data dumped successfully with UTF-8 encoding to data.json")

