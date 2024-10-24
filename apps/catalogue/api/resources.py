from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from ..models import Book

class BookResource(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        id     = row["id"]
        title  = row["title"]
        author = row["author"]
        publisher = row["publisher"]
        isbn     = row["isbn"]
        call_no  = row["call_no"]
        place_of_publication = row["place_of_publication"]
        year_published  = row["year_published"]
        institution     = row["institution"]

        # # Create New Object
        if not Book.objects.filter(title=title, author=author, institution=institution).exists:
            Book.objects.get_or_create(
                id=id,
                title=title, 
                author=author, 
                isbn=isbn, 
                call_no=call_no,
                publisher=publisher,
                institution=institution,
                year_published=year_published,
                place_of_publication=place_of_publication
            )
    
    class Meta:
        model = Book
        # skip_unchanged = True 
        # report_skipped = True
        fields = ['id', 'title', 'author', 'isbn', 'call_no', 'subject', 'publisher', 'place_of_publication', 'year_published', 'institution']
        exclude = ['edition', 'subject', 'edited', 'slug']