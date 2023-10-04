from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Book


class BookResource(resources.ModelResource):
    # author = fields.Field(column_name='author', attribute='author', widget=ForeignKeyWidget(Author, field='name'))
    
    def before_import_row(self, row, **kwargs):
        isbn         = row["isbn"]
        title        = row["title"]
        series       = row["series"]
        author       = row["author"]
        subject      = row["subject"]
        location     = row["location"]
        publisher    = row["publisher"]
        year_published = row["year_published"]
        call_number  = row["call_number"]

        # # Create New Object
        # Book.objects.get_or_create(
        #      title=title, author=author, 
        #      isbn=isbn,series=series,publisher=publisher,
        #      subject=subject, location=location, call_number=call_number,
        # )
    
    class Meta:
        model = Book
        skip_unchanged = True
        report_skipped = False
        fields = ["id", "title", 'subject', 'author', 'isbn', 'series','call_number', 'publisher', 'location', 'year_published', 'institution']