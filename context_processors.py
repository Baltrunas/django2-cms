from .models import Page, Tag


def page(request):
	try:
		page = Page.objects.get(public=True, url=request.path_info, sites__in=[request.site])
	except:
		page = None
	return {
		'tags': Tag.objects.all(),
		'page': page,
		'site': request.site,
		'url': request.path_info
	}
