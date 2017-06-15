from django_tables2.tables import Table
from django_tables2.columns import LinkColumn
from django_tables2.columns import TemplateColumn
from django_tables2.columns import Column
from django_tables2.utils import A  # alias for Accessor
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.conf.urls.static import static
from django.urls import reverse

from django.forms import CharField
from tinymce.widgets import TinyMCE

from models import ChipDesign
from models import SSHPublicKey

class IconLinkColumn(TemplateColumn):
	def __init__(self, title, url, icon, args=None, verbose_name=' ', **kwargs):
		super(IconLinkColumn, self).__init__(verbose_name, **kwargs)

	def header(self):
		return u'%s' % self.verbose_name

	def default(self):
		pass

	def render(self, record, table, value, bound_column, **kwargs):
		super(IconLinkColumn, self).render(record, table, value, bound_column, **kwargs)

		icon = '/static/img/' + self.icon + '.png'

		args = [a.resolve(record) if isinstance(a, A) else a for a in self.args]

		if args:
			url = reverse(self.url, args=args)
		else:
			url = reverse(self.url)

		html = '<a href="{url}" title="{title}"><img alt="{title}" src="{icon}" id="{icon_name}"/></a>'.format(title=self.title, url=url, icon=icon, icon_name=self.icon)

		return mark_safe(html)

class EditLinkIcon(IconLinkColumn):
	def __init__(self, url, args=None, verbose_name=' '):
		super(IconLinkColumn, self).__init__(url, args)
		self.icon = 'edit'
		self.args = args
		self.title = 'Edit'
		self.url = url
		self.verbose_name = verbose_name

class DeleteLinkIcon(IconLinkColumn):
	def __init__(self, url, args=None, verbose_name=' '):
		super(IconLinkColumn, self).__init__(url, args)
		self.icon = 'delete'
		self.args = args
		self.title = 'Delete'
		self.url = url
		self.verbose_name = verbose_name

class ChipDesignTable(Table):
	name = LinkColumn('work_bench_open', args=[A('id')])
	edit_link = EditLinkIcon(url='modify_design', args=[A('id')])
	delete_link = DeleteLinkIcon(url='delete_design', args=[A('id')])

	class Meta:
		model = ChipDesign
		fields = ('name', 'description') # fields to display
		attrs = {'class': 'table table-striped'}

class SSHKeyTable(Table):
	#save_link = LinkColumn('save_key', args=[A('id')], text='Edit', viewname='Miau1',)
	#delete_link = LinkColumn('delete_key', args=[A('id')], text='Delete', viewname='Miau2',)
	orderable = False

	class Meta:
		model = SSHPublicKey
		fields = ('key',) # fields to display
		attrs = {'class': 'table table-striped', 'id': 'key_table',}
