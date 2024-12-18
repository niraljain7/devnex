import os
import json
from django.utils import timezone 
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from library.models import Author, Book, BorrowRecord
from library.serializers import AuthorSerializer, BookSerializer, BorrowRecordSerializer
from library_management.celery import generate_report

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowRecordViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = BorrowRecordSerializer(data=request.data)
        if serializer.is_valid():
            book = Book.objects.get(id=serializer.validated_data['book'].id)
            if book.available_copies > 0:
                book.available_copies -= 1
                book.save()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"error": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='return')
    def return_book(self, request, pk=None):
        borrow_record = BorrowRecord.objects.get(id=pk)
        if borrow_record and not borrow_record.return_date:
            borrow_record.return_date = timezone.now()
            borrow_record.book.available_copies += 1
            borrow_record.book.save()
            borrow_record.save()
            return Response({"message": "Book returned successfully"})
        return Response({"error": "Invalid record or already returned"}, status=status.HTTP_400_BAD_REQUEST)

class ReportViewSet(viewsets.ViewSet):
    def list(self, request):
        if not os.path.exists("reports/report_latest.json"):
            return Response({"error": "No report generated"}, status=status.HTTP_400_BAD_REQUEST)

        with open("reports/report_latest.json") as h:
            report = json.load(h)
        return Response(report)

    def create(self, request):
        generate_report.delay()
        return Response({"message": "Report generation started"}, status=status.HTTP_202_ACCEPTED)
