from django.shortcuts import render
import requests
import json
from bs4 import BeautifulSoup as b
import re
from waterdebt.models import Post

# Defining templates
test = "test.html"
blog = "blog/blog.html"

def index(request):
	return render(request, test)

def waterdebt(request):
	c = {}
	l = []

	# c['error'] = "Zəhmət olmasa ilk öncə formu doldurub sonra borcu öyrən butonuna basın."

	abkodu = request.POST.get('abkodu')

	if abkodu:
		api = "http://data.e-gov.az/api/v1/IEGOVService.svc/GetDebtByAbonentCode/{}".format(abkodu)


	data = requests.get(api)

	d_d = json.loads(data.text)
	b_d = d_d['response']['htmlField']
	soup = b(b_d, 'html.parser')

	if len(soup.find_all('b')) == 0:
		c['error'] = """Abonent kodu ya yanlışdır ya da boş buraxılıb.
		Zəhmət olmasa kodunuzu yoxlayın və yenidən yazın"""

	else:
		for a in soup.find_all('b'):
			l.append(re.sub(r"[<b>,</b>]", "", str(a)))

		c['result'] = True
		c['code'] = "Abonent kodu: " + l[1]
		c['name'] = "Ad: " + l[3]
		c['debt'] = "Borc: " + l[5] + " AZN"


	return render(request, test, c)

def imei(request):
	c = {}

	imei = request.POST.get('imei')

	if imei:
		api = "http://data.e-gov.az/api/v1/IEGOVService.svc/CheckMobilImei/{}".format(imei)
		data = requests.get(api)

		d_d = json.loads(data.text)
		n = d_d['response']
		c['d'] = n
		return render(request, "test.html", c)
	else:
		c['d'] = "IMEI kodu ya səhvdir ya da boş buraxılıb."
		return render(request, "test.html", c)

def entry(request):
	post = Post.objects.all()[:10]
	context = {
		'post': post
	}
	return render(request, blog, context)