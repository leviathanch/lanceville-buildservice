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
	def __init__(self, title=None, url=None, jsfun=None, icon=None, args=None, verbose_name=' ', **kwargs):
		super(IconLinkColumn, self).__init__(verbose_name, **kwargs)
		self.icon = icon
		self.args = args
		self.verbose_name = verbose_name
		self.url = url
		self.jsfun = jsfun

	def header(self):
		return u'%s' % self.verbose_name

	def default(self):
		pass

	def render(self, record, table, value, bound_column, **kwargs):
		super(IconLinkColumn, self).render(record, table, value, bound_column, **kwargs)

		icon = '/static/img/' + self.icon + '.png'

		nargs = None
		if(self.args):
			nargs = [a.resolve(record) if isinstance(a, A) else a for a in self.args]
	
	
		if(self.jsfun):
			if(self.url):
				if nargs:
					jsurl = reverse(self.url, args=nargs)
				else:
					jsurl = reverse(self.url)
				url = 'javascript:'+self.jsfun+'('+jsurl+')'
			else:
				if nargs:
					url = 'javascript:'+self.jsfun+'('+str(nargs[0])
					for i in nargs[1:]:
						url+=','+str(i)
					url+=')'
				else:
					url = 'javascript:'+self.jsfun+'()'

		elif(self.url):
			if nargs:
				url = reverse(self.url, args=nargs)
			else:
				url = reverse(self.url)

		elif(self.jsfun):
			url = 'javascript:'+self.jsfun+'()'

		else:
			url = "\t"

		html = '<a href="{url}" title="{title}"><img alt="{title}" src="{icon}" id="{icon_name}"/></a>'.format(title=self.title, url=url, icon=icon, icon_name=self.icon)

		return mark_safe(html)

class EditLinkIcon(IconLinkColumn):
	def __init__(self, jsfun=None, url=None, args=None, verbose_name=' '):
		super(EditLinkIcon, self).__init__(jsfun=jsfun,url=url, args=args)
		self.title='Edit'
		self.icon='edit'


class DeleteLinkIcon(IconLinkColumn):
	def __init__(self, jsfun=None, url=None, args=None, verbose_name=' '):
		super(DeleteLinkIcon, self).__init__(jsfun=jsfun,url=url, args=args)
		self.title='Delete'
		self.icon='delete'

class ChipDesignTable(Table):
	id = Column(orderable=False, verbose_name='')
	name = LinkColumn('work_bench_open', args=[A('id')])
	edit_link = EditLinkIcon(url='modify_design', args=[A('id')])
	delete_link = DeleteLinkIcon(url='delete_design', args=[A('id')])

	class Meta:
		model = ChipDesign
		fields = ('name','technology','description','edit_link','delete_link','id') # fields to display
		attrs = {'class': 'table table-striped'}

class SSHKeyTable(Table):
	id = Column(orderable=False, verbose_name='')
	edit_link = EditLinkIcon(jsfun='editPubKey', args=[A('id')])
	delete_link = DeleteLinkIcon(url='delete_key', args=[A('id')])

	class Meta:
		model = SSHPublicKey
		fields = ('comment','key','edit_link','delete_link','id') # fields to display
		attrs = {'class': 'table table-striped', 'id': 'key_table',}
