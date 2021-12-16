from django.http import JsonResponse

from mainapp.forms import HobbiesMultiForm
from django.template.context_processors import csrf
from django.core.files.storage import FileSystemStorage
from .models import FriendRequest, Hobby, Profile, User
from .forms import ProfilePicForm, UpdateUserEmailForm
from django.http.response import HttpResponseBadRequest
from crispy_forms.utils import render_crispy_form
import json
from django.shortcuts import get_object_or_404
from django.core.files import File

from crispy_forms.utils import render_crispy_form

import json


from django.db.models import Count

from datetime import date
from dateutil.relativedelta import relativedelta


def friends_api(request):
    current_user = request.user
    requests  =  current_user.request_sent.all()

    a = current_user.hobby_set.all()
        #form = json.loads(request.body)
    currentName = current_user.username
    if request.method == 'GET':
        return JsonResponse({
            'requests_sent': [request.to_dict() for request in requests],
            'users': [User.to_dict() for User in User.objects.filter(hobby__in = a).exclude(username = currentName).annotate(itemcount=Count('id')).order_by('-itemcount')],
            'current_user': current_user.to_dict()
        })


def filters_api(request):
    # print("filter api called")
    current_user = request.user
    a = current_user.hobby_set.all()
    form = json.loads(request.body)
    currentName = current_user.username
    # print(a.get(id=1).name)
    # print(current_user.username)
    requests  =  current_user.request_sent.all()
    if request.method == 'POST':
        if form['age1'] is None:
            form['age1'] = 0
        if form['age2'] is None:
           form['age2'] = 100
        if form['city'] == '':
            # print("inside city is none")
            userForm = User.objects.filter(hobby__in = a,profile__dob__gt = date.today() - relativedelta(years=+(form['age2']+1)), profile__dob__lt = date.today() - relativedelta(years=+(int(form['age1'])))).exclude(username = currentName).annotate(itemcount=Count('id')).order_by('-itemcount')
        else:
            userForm = User.objects.filter(hobby__in = a,profile__dob__gt = date.today() - relativedelta(years=+form['age2']+1), profile__dob__lt = date.today() - relativedelta(years=+form['age1']), profile__city = form['city']).exclude(username = currentName).annotate(itemcount=Count('id')).order_by('-itemcount')    
        
        #filteredUser = userForm.objects.filter(profile__age <= form['age2'] & profile__age >= form['age1'])
        # print("max age: ", date.today() - relativedelta(years=+form['age2']))
        # print("min age: ", date.today() - relativedelta(years=+form['age1']))
        return JsonResponse({
            'requests_sent': [request.to_dict() for request in requests],
            'users': [User.to_dict() for User in userForm],
            'current_user': current_user.to_dict()
            
        })


def get_current_user_hobby (request):
    current_user  =  request.user
    if request.method  == 'GET':
        return JsonResponse({
            'current_user': current_user.to_dict()

        })
    
def create_new_hobby(request):
    if request.method == "POST":
        current_user = request.user
       
        post_data = json.loads(request.body.decode("utf-8"))
        name_hobby = post_data.get('hobby')
        print("Something" + str(name_hobby))
        hobby  =  Hobby(name= name_hobby)

        hobby.save()
        hobby.users.add(current_user)

        new_form  = HobbiesMultiForm()
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(new_form, context=ctx)
        return JsonResponse({
            'current_user': current_user.to_dict(),
            'hobby_form' :  form_html

        })
    




def add_new_hobby(request):
    current_user = request.user
    data  =   json.loads(request.body.decode("utf-8"))
    #current_user.hobby_set.clear()
    hobby_ids  = data["hobbies"]
    
    for id in hobby_ids:
        print(id)
        current_user.hobby_set.add(get_object_or_404(Hobby, id = id))
    current_user.save()
    return JsonResponse({
            'current_user': current_user.to_dict()
        })


def delete_hobby_from_user (request, hobby_id):
    current_user  =  request.user
    if request.method  == "DELETE":
        hobby  =  get_object_or_404(Hobby, id =  hobby_id)
        current_user.hobby_set.remove (hobby)
        current_user.save()

        return JsonResponse({
             'current_user': current_user.to_dict()
        })





def get_friends_requests(request):
    current_user = request.user
    requests  =  current_user.request_received.all()
    if request.method == 'GET':
        return JsonResponse({
            'requests': [request.to_dict() for request in requests],
            'current_user': current_user.to_dict()
        })


def send_friends_request(request, to_user_id):
    if request.method ==  'POST':
        current_user = request.user
        print(current_user)
        receiver =  get_object_or_404(User, id= to_user_id)
        print(receiver)
        newRequest  =  FriendRequest(from_user = current_user,to_user=receiver)
        newRequest.save()
        print(newRequest)

        requests  =  current_user.request_sent.all()
        return JsonResponse({
                'requests_sent': [request.to_dict() for request in requests],
            })
    else :
        print("Something")


def accept_request(request):
    if request.method == 'POST':
        current_user = request.user
        post_data = json.loads(request.body.decode("utf-8"))
        userId  =  post_data["id"]
        other_user  =  get_object_or_404(User, id=userId)
        current_user.friends.add(other_user)
        current_user.request_received.filter(from_user = other_user.id).delete()
        other_user.request_received.filter(from_user = current_user.id).delete()
        current_user.save()
        other_user.save()
        requests  =  current_user.request_received.all()
        return JsonResponse({
            'requests': [request.to_dict() for request in requests],
            'users': [User.to_dict() for User in User.objects.all()],
            'current_user': current_user.to_dict()
        })
       


def decline_request(request):
    if request.method == 'POST':
        current_user = request.user
        post_data = json.loads(request.body.decode("utf-8"))
        userId  =  post_data["id"]
        other_user  =  get_object_or_404(User, id=userId)
        current_user.request_received.filter(from_user = other_user.id).delete()
        other_user.request_received.filter(from_user = current_user.id).delete()
        current_user.save()
        other_user.save()
        requests  =  current_user.request_received.all()
        return JsonResponse({
            'requests': [request.to_dict() for request in requests],
            'users': [User.to_dict() for User in User.objects.all()],
            'current_user': current_user.to_dict()
        })
       



def update_user_info(request):

    if request.method == 'POST' :

        current_user =  request.user
        value  = request.FILES.get('profilePic')
        if value:
            myfile = request.FILES['profilePic']
            current_user.profile.image.save(myfile.name, myfile,True) 
   
        

 
        email  =  request.POST['emailUser']
   
        dob =  request.POST['dobUser']
        city =  request.POST['cityUser']
        
   
    
        current_user.email =  email
        current_user.profile.dob =  dob
        current_user.profile.city =  city
        current_user.profile.save()
     
        # fs = FileSystemStorage(location='media/profile_images/')
        current_user.save()
        return JsonResponse({
            'current_user': current_user.to_dict(),
            })


    # if request.method   == 'POST':
     
    #     form = ProfilePicForm(request.POST , request.FILES, instance=request.user.profile)
    #     email_form =  UpdateUserEmailForm(request.POST, instance=request.user )

    #     if form.is_valid():
    #         #email_form.save()
    #         print(form)
    #         form.save()
    #         new_email_form = UpdateUserEmailForm(instance=request.user)
    #         new_profile_form =  ProfilePicForm(instance=request.user.profile)
    #         ctx = {}
    #         ctx.update(csrf(request))
    #         form_html_email = render_crispy_form(new_email_form, context=ctx)
    #         new_profile_form = render_crispy_form(new_profile_form, context=ctx)
    #         current_user = request.user
    #         return JsonResponse({
    #             'current_user': current_user.to_dict(),
    #             'email_form' :  form_html_email,
    #             'profile_form' :  new_profile_form



    #         })
    #     else :
            # print(form.errors.as_data()) # here you print errors to terminal




