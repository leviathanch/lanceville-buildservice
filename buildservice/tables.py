from django_tables2.tables import Table
from django_tables2.columns import LinkColumn
from django_tables2.columns import Column
from django_tables2.utils import A  # alias for Accessor
from django.utils.safestring import mark_safe
from django.utils.html import escape

from django.forms import CharField
from tinymce.widgets import TinyMCE

from models import ChipDesign
from models import SSHPublicKey

class BaseIconLinkColumn(Column):
	def __init__(self, attrs=None, text=None, *args, **kwargs):
		kwargs['attrs'] = attrs
		self.text = text
		super(BaseIconLinkColumn, self).__init__(*args, **kwargs)

	def text_value(self, record, value):
		if self.text is None:
			return value

		return self.text(record) if callable(self.text) else self.text

	def render_link(self, uri, record, value, attrs=None):
		'''
		Render a hyperlink.

		Arguments:
		uri (str): URI for the hyperlink
		record: record currently being rendered
		value (str): value to be wrapped in ``<a></a>``, might be overridden
			by ``self.text``
		attrs (dict): ``<a>`` tag attributes
		'''
		attrs = AttributeDict(attrs if attrs is not None else self.attrs.get('a', {}))
		attrs['href'] = uri

		return format_html('<a {attrs}>{text}</a>', attrs=attrs.as_html(), text=self.text_value(record, value))

	def value(self, record, value):
		'''
		Returns the content for a specific cell similarly to `.render` however
		without any html content.
		'''
		return self.text_value(record, value)

class IconLinkColumn(BaseIconLinkColumn):
	def __init__(self, viewname=None, urlconf=None, args=None, kwargs=None, current_app=None, attrs=None, **extra):
		super(IconLinkColumn, self).__init__(attrs, **extra)
		self.viewname = viewname
		self.urlconf = urlconf
		self.args = args
		self.kwargs = kwargs
		self.current_app = current_app

	def compose_url(self, record, *args, **kwargs):
		'''Compose the url if the column is constructed with a viewname.'''

		if self.viewname is None:
			if not hasattr(record, 'get_absolute_url'):
				raise TypeError('if viewname=None, record must define a get_absolute_url')
			return record.get_absolute_url()

		def resolve_if_accessor(val):
			return val.resolve(record) if isinstance(val, Accessor) else val

		viewname = resolve_if_accessor(self.viewname)

		# Collect the optional arguments for django's reverse()
		params = {}
		if self.urlconf:
			params['urlconf'] = resolve_if_accessor(self.urlconf)
		if self.args:
			params['args'] = [resolve_if_accessor(a) for a in self.args]
		if self.kwargs:
			params['kwargs'] = {key: resolve_if_accessor(val) for key, val in self.kwargs.items()}
		if self.current_app:
			params['current_app'] = resolve_if_accessor(self.current_app)

		return reverse(viewname, **params)

	def render(self, value, record, bound_column):
		return self.render_link(
			self.compose_url(record, bound_column),
			record=record,
			value=value
		)

#	def __init__(self, icon=None, urlconf=None, args=None, kwargs=None, current_app=None, attrs=None, **extra):
#		self.icon = icon
#		super(IconLinkColumn, self).__init__(*args)

#	def render(self, value, record, bound_column):
		#picture_url = mark_safe('<img src="/static/img/%s.jpg" />' % escape(self.icon))
#		return "Miau"
		#return self.render_link(
		#	uri=self.compose_url(record, bound_column),
		#	icon_url=picture_url
		#)

	#def render_link(self, uri, icon_url, attrs=None):
	#	attrs = AttributeDict(attrs if attrs is not None else self.attrs.get('a', {}))
	#	attrs['href'] = uri
	#	return format_html('<a {attrs}>{icon}</a>', attrs=attrs.as_html(), text=icon_url)

class ChipDesignTable(Table):
	name = LinkColumn('work_bench_open', args=[A('id')])
	edit_link = IconLinkColumn('modify_design', args=[A('id')], verbose_name='Miau1')
	#delete_link = IconLinkColumn('delete_design', args=[A('id')], icon='delete', viewname='Miau2')
	orderable = False

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
