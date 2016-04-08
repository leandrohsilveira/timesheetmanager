'''
Created on 8 de abr de 2016

@author: Leandro
'''
from django.shortcuts import redirect
def index(request):
	return redirect("identity:current_user_detail")
