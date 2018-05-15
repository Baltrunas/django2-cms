from .models import Page


def page(request):
	try:
		page = Page.objects.get(public=True, url=request.path_info, sites__in=[request.site])
	except:
		page = None
	return {
		'page': page,
		'site': request.site,
		'url': request.path_info
	}
