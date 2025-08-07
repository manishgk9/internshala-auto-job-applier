from django.urls import include, path
from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    GetMatchingJobsView, SearchQueryView, ApplyJobsView,
    AppliedJobsView
)

router=DefaultRouter()
router.register(r'applied-jobs', AppliedJobsView, basename='applied-jobs')
urlpatterns = [
    path('api/get-matching-jobs', GetMatchingJobsView.as_view(), name='get-matching-jobs'),
    path('api/search-query/<str:query>', SearchQueryView.as_view(), name='search-query'),
    path('api/apply', ApplyJobsView.as_view(), name='apply-jobs'),
    path('api/', include(router.urls)),
]