"""End-to-end test that verifies django-counter-field works with a fresh Django project."""

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def test_e2e_django_project():
    """Create a fresh Django project and verify django-counter-field works correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)

        # Create a new Django project
        result = subprocess.run(
            ["django-admin", "startproject", "testproject", "."],
            cwd=project_dir,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Failed to create Django project: {result.stderr}"

        # Create a test app
        result = subprocess.run(
            [sys.executable, "manage.py", "startapp", "testapp"],
            cwd=project_dir,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Failed to create app: {result.stderr}"

        # Update settings.py to include the app and django_counter_field
        settings_file = project_dir / "testproject" / "settings.py"
        settings_content = settings_file.read_text()
        settings_content = settings_content.replace(
            "INSTALLED_APPS = [",
            "INSTALLED_APPS = [\n    'django_counter_field',\n    'testapp',",
        )
        settings_file.write_text(settings_content)

        # Create models that use CounterField
        models_file = project_dir / "testapp" / "models.py"
        models_file.write_text(
            """
from django.db import models
from django_counter_field import CounterField, CounterMixin, connect_counter


class Author(models.Model):
    name = models.CharField(max_length=100)
    book_count = CounterField()


class Book(CounterMixin, models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


connect_counter('book_count', Book.author)
"""
        )

        # Create a test script that exercises the functionality
        test_script = project_dir / "run_test.py"
        test_script.write_text(
            """
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testproject.settings')
django.setup()

from django.core.management import call_command

# Create migrations and apply them
call_command('makemigrations', 'testapp', verbosity=0)
call_command('migrate', verbosity=0)

from testapp.models import Author, Book

# Test counter functionality
author = Author.objects.create(name='Test Author')
assert author.book_count == 0, f"Expected 0, got {author.book_count}"

# Create a book
book = Book.objects.create(title='Test Book', author=author)
author.refresh_from_db()
assert author.book_count == 1, f"Expected 1, got {author.book_count}"

# Create another book
book2 = Book.objects.create(title='Test Book 2', author=author)
author.refresh_from_db()
assert author.book_count == 2, f"Expected 2, got {author.book_count}"

# Delete a book
book.delete()
author.refresh_from_db()
assert author.book_count == 1, f"Expected 1, got {author.book_count}"

print("All e2e tests passed!")
"""
        )

        # Run the test script with a clean environment (no inherited DJANGO_SETTINGS_MODULE)
        env = {k: v for k, v in os.environ.items() if k != "DJANGO_SETTINGS_MODULE"}
        result = subprocess.run(
            [sys.executable, str(test_script)],
            cwd=project_dir,
            capture_output=True,
            text=True,
            env=env,
        )

        if result.returncode != 0:
            raise AssertionError(
                f"E2E test failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
            )

        assert "All e2e tests passed!" in result.stdout
