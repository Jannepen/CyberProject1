from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
from .models import Account
 
 
@login_required
@transaction.atomic
@csrf_exempt
def transferView(request):
	
	if request.method == 'POST':
		user = request.user

		#Flaw: allows injection
		to_username = request.POST.get('to')
		query = f"SELECT * FROM auth_user WHERE username = '{to_username}'"
		to = User.objects.raw(query)[0]

		#Fix for injection: comment 3 lines above an uncomment line below to fix
		#to = User.objects.get(username=request.POST.get('to'))

		amount = int(request.POST.get('amount'))

		if amount >= 0 and user.account.balance >= amount:
			user.account.balance -= amount
			to.account.balance += amount
			
 
		user.account.save()
		to.account.save()
	
	return redirect('/')
 

#Flaw: Broken access control
#Fix: uncomment line below
#@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts})