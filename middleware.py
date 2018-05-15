import re

from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.conf import settings

from django.middleware.locale import LocaleMiddleware
from django.utils import translation

from .views import page
from .models import Page, Redirect

class PageMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)

		if response.status_code != 404:
			return response

		try:
			return page(request, request.path_info)
		except Http404:
			return response
		except Exception:
			if settings.DEBUG:
				raise
			return response

	# def process_exception(self, request, exception):
	# 	print ('process_exception')
	# 	context = {}
	# 	return render(request, '404.html', context)

	def process_template_response(self, request, response):
		print ('process_template_response')
		try:
			page = Page.objects.get(public=True, url=request.path_info, sites__in=[request.site])
			if page.template:
				response.template_name = page.template
		except:
			pass

		return response


class SwitchLocale(LocaleMiddleware):
	def process_request(self, request):
		if hasattr(request.site, 'settings'):
			language = request.site.settings.language
		else:
			language = settings.LANGUAGE_CODE

		translation.activate(language)
		request.LANGUAGE_CODE = language


class Redirects(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		from_domain = request.get_host()
		from_url = request.path_info

		if request.is_secure():
			from_protocol = 'https://'
		else:
			from_protocol = 'http://'

		redirect_list = Redirect.objects.filter(from_domain=from_domain, from_protocol=from_protocol, public=True)

		for redirect in redirect_list:
			if redirect.regex:
				try:
					redirect_re = re.compile(redirect.from_url)
					if redirect_re.findall(from_url):
						to_url = re.sub(redirect.from_url, redirect.to_url, from_url)
						result_url = redirect.to_protocol + redirect.to_domain + to_url
						return HttpResponsePermanentRedirect(result_url)
				except:
					pass
			elif redirect.from_url == from_url:
				result_url = redirect.to_protocol + redirect.to_domain + redirect.to_url
				return HttpResponsePermanentRedirect(result_url)

		return self.get_response(request)
