from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	profile_picture = models.ImageField(upload_to='profile_images/', null=True)
	profile_image_name = models.CharField(max_length=200, blank=True)
	ban_status = models.BooleanField(default=0)
	ipv4_address = models.CharField(max_length=16, blank=True)
	user_role = models.CharField(max_length=250, default="Member")
	user_occupation = models.CharField(max_length=250, blank=True)
	user_bio = models.CharField(max_length=300, blank=True)
	warning_points = models.IntegerField(default=0)
	followers = models.IntegerField(default=0)
	following = models.IntegerField(default=0)
	total_users_blocked = models.IntegerField(default=0)

	def serialize(self):
		return {
		"first_name": self.first_name,
		"last_name": self.last_name,
		"user_role": self.user_role,
		"user_occupation": self.user_occupation,
		"user_bio": self.user_bio,
		}


class upload_image(models.Model):
	upload_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_upload")
	image_name = models.CharField(max_length=100, blank=True)
	main_image_name = models.CharField(max_length=100, blank=True)
	images = models.ImageField(upload_to='uploads/')
	upload_date = models.DateTimeField(auto_now_add=True)
	visibility_status = models.IntegerField(default=1)
	likes = models.IntegerField(default=0)
	categories = models.CharField(max_length=20, blank=True)
	image_description = models.CharField(max_length=250)

	def serialize(self):
		return {
		"id": self.id,
		"upload_by": self.upload_by.username,
		"uploader_id": self.upload_by.id,
		"image_location": self.upload_by.profile_image_name,
		"image_name": self.image_name,
		"main_image_name": self.main_image_name,
		"upload_date": self.upload_date,
		"visibility_status": self.visibility_status,
		"likes": self.likes,
		"categories": self.categories,
		"image_description": self.image_description
		}


class image_comments(models.Model):
	commented_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commented_user')
	comment = models.CharField(max_length=250)
	comment_time = models.DateTimeField(auto_now_add=True)
	image_id = models.ForeignKey(upload_image, on_delete=models.CASCADE, related_name='commented_image_id')

	def serialize(self):
		return {
			"id": self.id,
			"commented_by": self.commented_by.username,
			"commented_by_id": self.commented_by.id,
			"image_location": self.commented_by.profile_image_name,
			"comment": self.comment,
			"comment_time": self.comment_time,
		}

class image_like(models.Model):
	liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
	image_liked = models.ForeignKey(upload_image, on_delete=models.CASCADE, related_name='liked_image')
	liked_time = models.DateTimeField(auto_now_add=True)

	def serialize(self):
		return {
		"liked_by": self.liked_by.id,
		"image_liked": self.image_liked.id,
		"liked_time": self.liked_time,
		}

class follows(models.Model):
	followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user")
	followed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_by")
	follow_date = models.DateTimeField(auto_now_add=True)