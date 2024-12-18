
import os
import json
import django
from celery import Celery
from datetime import datetime


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management.settings')
app = Celery('library_management')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

django.setup()
from library.models import Book, BorrowRecord, Author


@app.task
def generate_report():

    report = dict()

    report["total_number_of_authors"] = Author.objects.all().count()
    report["total_number_of_books"] = Book.objects.all().count()
    report["total_number_of_books_currently_borrowed"] = BorrowRecord.objects.filter(return_date=None).count()

    date_string = datetime.now().date().strftime('%Y%m%d')
    filename = f"reports/report_{date_string}.json"

    with open(filename, "w") as h:
        h.write(json.dumps(report, indent=4))
    
    with open("reports/report_latest.json", "w") as h:
        h.write(json.dumps(report, indent=4))
