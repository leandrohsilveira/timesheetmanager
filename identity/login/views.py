'''
Created on 21 de mar de 2016

@author: Leandro
'''
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import logout_then_login
from django.shortcuts import redirect


def fazer_login(request):
	username = request.POST["username"];
	password = request.POST["password"];
	nextUrl = request.POST["next"];

	user = authenticate(username = username, password = password);
	if user:
		if user.is_active:
			login(request, user);
			if nextUrl:
				return redirect(nextUrl);
			else:
				return redirect("identity:index")
	return redirect("/identity/login?next=%s" % (nextUrl));

def fazer_logout(request):
	return logout_then_login(request);
