from django.shortcuts import render
from .models import Subscriber
from django.http import HttpResponseRedirect
# Create your views here.


def homepage_subscription(request):
	if request.method == 'GET':
		return render(request, "index.html")

	elif request.method == 'POST':
		try:
			email = request.POST['email']
			if not Subscriber.objects.filter(email_address=email):
				Subscriber.objects.create(email_address=email)
				text = 'You successfully subscribed to our beta version!'
			else:
				text = 'You had already subscribed to our beta version!'
			return render(request, "index.html", {
					'submitted' : text
					})
		except Exception as e:
			print(e)
			return HttpResponseRedirect("/")