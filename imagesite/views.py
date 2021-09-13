import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator
import mimetypes
import os
from PIL import Image
from .models import *

# Create your views here.
def index(request):
	return render(request, "index.html")

def compress(name, amount):
    basewidth = 300
    picture = Image.open(name)
    wpercent = (basewidth / float(picture.size[0]))
    hsize = int((float(picture.size[1]) * float(wpercent)))
    picture = picture.resize((basewidth, hsize), Image.ANTIALIAS)
    picture.save('compressed_images/'+name, format=None,
        optimize=True,
        quality=amount)
    return

def check_image_size(image_name):
    quality=100
    print(os.getcwd())
    os.chdir('imagesite/static/images/uploads')
    # file_size = os.path.getsize(image_name)
    # if file_size > 400000:
    #     quality=10
    # else:
    #     quality=80

    compress(image_name, quality)



def upload_images(request):
    if not request.user.id:
        return HttpResponseRedirect(reverse("login"))
        
    current_user = User.objects.get(id=request.user.id)
    if request.method =="POST":
        image_name = request.POST["image-name"]
        main_image_name = request.POST["main-image-name"]
        image_description = request.POST["image-description"]
        category = request.POST["category_name"]
        is_private = request.POST.get('visible', 0)
        if is_private == 'on':
            is_private = 1
        image = request.FILES["image"]
        upload_image(upload_by=current_user, image_name=image_name, main_image_name=main_image_name,images=image, image_description=image_description, visibility_status=is_private, categories=category).save()
        check_image_size(main_image_name)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "upload_image.html")

def posted_image(request, user_id):
    if user_id == "all":
        start = int(request.GET.get("start"))
        end = int(request.GET.get("end"))
        image_posted = upload_image.objects.filter(visibility_status=0)
        image_posted = image_posted.order_by("-upload_date").all()

        if end > len(image_posted):
            end = len(image_posted)
        new_posted = []
        print(f"{start} {end}")
        for i in range(start - 1, end):
            new_posted.append(image_posted[i])
            print(new_posted)
        return JsonResponse([post.serialize() for post in new_posted], safe=False)
    
    start = int(request.GET.get("start"))
    end = int(request.GET.get("end"))
    user_id = int(user_id)
    image_posted = upload_image.objects.filter(upload_by=user_id)
    image_posted = image_posted.order_by("-upload_date").all()
    if end > len(image_posted):
        end = len(image_posted)
    new_posted = []
    for i in range(start - 1, end):
        new_posted.append(image_posted[i])
        print(new_posted)
    return JsonResponse([post.serialize() for post in new_posted], safe=False)


def category_page(request, category):
    return render(request, "category.html", {
        "message": category,
        })

def image_category(request, category_name):
    image_category = upload_image.objects.filter(categories=category_name, visibility_status=0)
    image_category = image_category.order_by("-upload_date").all()
    return JsonResponse([post.serialize() for post in image_category], safe=False)


def user_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        user = None

    try:
        check_follow = follows.objects.get(followed_user=user_id, followed_by=request.user.id)
    except:
        check_follow = None
    if not user:
        return render(request, 'error.html', {
            "ErrorMessage": "Error 404: No user found",
            })
    image_posts = upload_image.objects.filter(upload_by=user_id)
    post_length = len(image_posts)
    return render(request, 'user_profile.html', {
        "user": user,
        "check_follow": check_follow,
        "post_amount": post_length,
        })

def edit_profile(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        profile_image_name = request.POST["profile_picture_name"]
        first_name = request.POST["first_name"]
        if not first_name:
            first_name = request.user.first_name

        last_name = request.POST["last_name"]
        if not last_name:
            last_name = request.user.last_name
            
        occupation = request.POST["user_occupation"]
        if not occupation:
            occupation = request.user.user_occupation

        bio = request.POST["user_bio"]
        if not bio:
            bio = request.user.user_bio

        main_user = User.objects.get(id=request.user.id)
        try:
            image = request.FILES["image"]
        except:
            image = None

        if image:
            main_user.first_name = first_name 
            main_user.last_name = last_name 
            main_user.user_occupation = occupation 
            main_user.user_bio = bio 
            main_user.profile_picture = image
            main_user.profile_image_name = profile_image_name
            main_user.save()
            return render(request, "index.html")
        else:    
            main_user.first_name = first_name 
            main_user.last_name = last_name 
            main_user.user_occupation = occupation 
            main_user.user_bio = bio 
            main_user.save()
            return render(request, "index.html")
    return render(request, "edit_profile.html", {
        "profile": user,
        })

def like_image(request, user_id):
    try:
        liked_image = upload_image.objects.get(id=user_id)     
    except:
        liked_image = None
        
    try:
        check_liked = image_like.objects.get(liked_by=request.user.id, image_liked=user_id)
    except:
        check_liked = None

    if check_liked:
        check_liked.delete()
        liked_image.likes = liked_image.likes - 1
        liked_image.save()
        return JsonResponse(f"Success: Image {user_id} Unliked successfully", safe=False)
    else:
        liked_by = User.objects.get(id=request.user.id)
        image_like(liked_by=liked_by, image_liked=liked_image).save()
        liked_image.likes = liked_image.likes + 1
        liked_image.save()
        return JsonResponse(f"Success: Image {user_id} liked successfully", safe=False)
    return JsonResponse(f"Not success: Image {user_id} liked Unsuccessfully", safe=False)

def check_like(request, image_id):
    try:
        checks = image_like.objects.get(liked_by=request.user.id, image_liked=image_id)
    except:
        return JsonResponse("Escept False", safe=False)
    if checks:
        return JsonResponse(checks.serialize(), safe=False)
    return JsonResponse("False", safe=False)

def view_image(request, image_id):
    try:
        image_id=int(image_id)
        image = upload_image.objects.get(id=image_id)
        return render(request, "view_image.html", {
            "image": image,
            })
    except:
        return render(request, "error.html", {
            "ErrorMessage": "Error 404: No image found!"
            })

def follow_user(request, user_id):
    try:
        follow_check = follows.objects.get(followed_user=user_id, followed_by=request.user.id)
    except:
        follow_check = None

    if follow_check:
        follow_check.delete()
        followed_user = User.objects.get(id=user_id)
        followed_by = User.objects.get(id=request.user.id)
        followed_user.followers = followed_user.followers - 1
        followed_by.following = followed_by.following - 1
        followed_user.save()
        followed_by.save()
        return JsonResponse(f"User {user_id} has been Unfollowed", safe=False)
    try:
        followed_user = User.objects.get(id=user_id)
        followed_by = User.objects.get(id=request.user.id)
        follows(followed_by=followed_by, followed_user=followed_user).save()
        followed_user.followers = followed_user.followers + 1
        followed_by.following = followed_by.following + 1
        followed_user.save()
        followed_by.save()
        return JsonResponse(f"User {user_id} has been followed", safe=False)
    except:
        return JsonResponse(f"User {user_id} cannot be followed", safe=False)
    return JsonResponse(f"User {user_id} has already been followed", safe=False)

def download_image(request, image_name):
    fl_path = 'imagesite/static/images/uploads/'
    filename = image_name
    image_path = fl_path + image_name
    print(os.getcwd())
    fl = open(image_path, 'rb')
    mime_type, _= mimetypes.guess_type(image_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def comment_image(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)

    comment = data.get("comment", "")
    imageid = data.get("image_id", "")
    image_id = upload_image.objects.get(id = int(imageid))
    commented_by = User.objects.get(id=request.user.id)
    image_comments(commented_by=commented_by, comment=comment, image_id=image_id).save()
    return JsonResponse({"message": "Comment added successfully."}, status=201)

def get_comment(request, image_id):
    comments = image_comments.objects.filter(image_id=image_id)
    comments = comments.order_by("-comment_time").all()
    return JsonResponse([comment.serialize() for comment in comments], safe=False)


def following(request):
    followed = follows.objects.filter(followed_by=request.user.id)
    followedid = []
    for follow in followed:
        followedid.append(follow.followed_user.id)
    followedpost = upload_image.objects.filter(upload_by__in=followedid)
    followedpost = followedpost.order_by("-upload_date").all()
    postpage = Paginator(followedpost, 10)
    followpost = postpage.page(1)
    return render(request, "following.html", {
        "following_post": followpost,
        })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username or password."
            })
    else:
        if request.user.id != None:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["register-username"]
        email = request.POST["email"]
        password = request.POST["register-password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "login.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "login.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "login.html")