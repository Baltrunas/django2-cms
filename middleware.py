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


class SwitchLocale:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		LOCALE_SPECIFIC_URL = getattr(settings, 'LOCALE_SPECIFIC_URL', 'domain')
		LOCALE_DEFAULT = getattr(settings, 'LOCALE_DEFAULT', 'de')
		LOCALE_EXCLUDE = getattr(settings, 'LOCALE_EXCLUDE', [])
		LANGUAGES = getattr(settings, 'LANGUAGES')


		if LOCALE_SPECIFIC_URL == 'domain':
			if hasattr(request.site, 'settings'):
				language = request.site.settings.language
			else:
				language = settings.LANGUAGE_CODE

			translation.activate(language)
			request.LANGUAGE_CODE = language

			response = self.get_response(request)


		elif LOCALE_SPECIFIC_URL == 'dir':
			url = request.path_info
			lang = LOCALE_DEFAULT

			replace = True
			for EX_URL in LOCALE_EXCLUDE:
				if url.startswith(EX_URL):
					replace = False

			if replace:
				#  def withoud dir
				for lk in LANGUAGES:
					if url.startswith('/' + lk[0] + '/') and lk[0] != LOCALE_DEFAULT:
						lang = lk[0]
						request.path_info = url[3:]

				translation.activate(lang)
				request.LANGUAGE_CODE = lang

				response = self.get_response(request)

				if lang != LOCALE_DEFAULT:
					response.content = re.sub(b"<a (.*?) (href)='/", rb"<a \1 href='/" + bytes(lang + '/', 'utf-8'), response.content)
					response.content = re.sub(b'<a (.*?) (href)="/', rb'<a \1 href="/' + bytes(lang + '/', 'utf-8'), response.content)

				for lk in LANGUAGES:
					lng = bytes(lk[0], 'utf-8')
					if request.GET.urlencode():
						rget = bytes('?' + request.GET.urlencode(), 'utf-8')
					else:
						rget = b''
					if lk[0] == LOCALE_DEFAULT:
						response.content = re.sub(b'<a (.*?) href="lang-' + lng + b'"', rb'<a \1 href="' + bytes(request.path_info, 'utf-8') + b'"' + rget, response.content)
					else:
						response.content = re.sub(b'<a (.*?) href="lang-' + lng + b'"', rb'<a \1 href="/' + lng + bytes(request.path_info, 'utf-8') + b'"' + rget, response.content)

			else:
				response = self.get_response(request)

		return response



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
