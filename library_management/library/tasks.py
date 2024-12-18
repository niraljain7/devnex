import json
from datetime import datetime
from celery import shared_task
from library.models import Book, BorrowRecord, Author

@shared_task
def generate_report():

    report = dict()

    report["total_number_of_authors"] = Author.objects.all().count()
    report["total_number_of_books"] = Book.objects.all().count()
    report["total_number_of_books_currently_borrowed"] = BorrowRecord.objects.filter(return_date=None).count()

    date_string = datetime.now().date().strftime('%Y%m%d')
    filename = f"report_{date_string}.json"

    with open(filename, "w") as h:
        h.write(json.dumps(report, indent=4))
    
    with open("report_latest.json", "w") as h:
        h.write(json.dumps(report, indent=4))




