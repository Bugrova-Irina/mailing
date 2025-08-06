from django.core import serializers
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Export users to JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output", type=str, default="users_export.json", help="Output file name"
        )

    def handle(self, *args, **options):
        output_file = options["output"]
        users = User.objects.all()

        with open(output_file, "w", encoding="utf-8") as f:
            serializers.serialize("json", users, stream=f)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully exported {len(users)} users to {output_file}"
            )
        )
