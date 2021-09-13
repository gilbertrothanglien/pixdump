from . import views
from django.urls import path

urlpatterns = [
	path("", views.index, name="index"),
	path("upload_images", views.upload_images, name="upload_images"),
	path("user_profile/<int:user_id>", views.user_profile, name="user_profile"),
	path("edit_profile", views.edit_profile, name="edit_profile"),
	path("posted_image/<str:user_id>", views.posted_image, name="posted_image"),
	path("check_like/<int:image_id>", views.check_like, name="check_like"),
	path("like_image/<int:user_id>", views.like_image, name="like_image"),
	path("view_image/<int:image_id>", views.view_image, name="view_image"),
	path("follow_user/<int:user_id>", views.follow_user, name="follow_user"),
	path("image_category/<str:category_name>", views.image_category, name="image_category"),
	path("category/<str:category>", views.category_page, name="category_page"),
	path("following", views.following, name="following"),
	path("download_image/<str:image_name>", views.download_image, name="download_image"),
	path("comment_image", views.comment_image, name="comment_image"),
	path("get_comment/<int:image_id>", views.get_comment, name="get_comment"),
	path("login", views.login_view, name="login"),
	path("register", views.register, name="register"),
	path("logout", views.logout_view, name="logout"),
]