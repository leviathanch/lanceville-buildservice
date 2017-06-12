from django_tables2.tables import Table
from django_tables2.columns import LinkColumn
from django_tables2.utils import A  # alias for Accessor

from models import ChipDesign

class ChipDesignTable(Table):
	delete_link = LinkColumn('delete_design', args=[A('id')], text='Delete')
	edit_link = LinkColumn('modify_design', args=[A('id')], text='Edit')
	orderable = False
	class Meta:
		model = ChipDesign
		fields = ('name', 'url', 'description','delete_link') # fields to display
		attrs = {'class': 'table table-striped'}
