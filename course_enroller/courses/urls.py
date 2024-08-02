from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("enter_preferences/", views.enter_preferences, name="enter_preferences"),
    path("preferences_success/", views.preferences_success, name="preferences_success"),
    path("perform_allocation/", views.perform_allocation, name="perform_allocation"),
    path("allocation_results/", views.allocation_results, name="allocation_results"),
    path("clear_data/", views.clear_data, name="clear_data"),
    path("clear_success/", views.clear_success, name="clear_success"),
    path("sample_results/", views.sample_results, name="sample_results"),
    path(
        "sample_generation_success/",
        views.sample_generation_success,
        name="sample_generation_success",
    ),
    path("about/", views.about, name="about"),
    path("course_list/", views.course_list, name="course_list"),
]
