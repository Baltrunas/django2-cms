from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_protect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponse, Http404


from .models import Page


@csrf_protect
def page(request, url):
	context = {}

	page = get_object_or_404(Page, url=url, sites__in=[request.site])
	context['page'] = page

	# Pagination
	pages_list = Page.objects.filter(public=True, parent=page)
	page_number = request.GET.get('page', None)

	paginator = Paginator(pages_list, page.per_page)
	try:
		pages_list = paginator.page(page_number)
	except PageNotAnInteger:
		pages_list = paginator.page(1)
	except EmptyPage:
		pages_list = paginator.page(paginator.num_pages)

	context['pages_list'] = pages_list

	# Template
	if page.template:
		template = page.template
	else:
		template = 'cms/page.html'

	return render(request, template, context)


def robots_txt(request):
	if hasattr(request.site, 'settings'):
		return HttpResponse(request.site.settings.robots_txt, content_type='text/plain')
	else:
		raise Http404


def sitemap_xml(request):
	if hasattr(request.site, 'settings'):
		return HttpResponse(request.site.settings.sitemap_xml, content_type='text/xml')
	else:
		raise Http404
