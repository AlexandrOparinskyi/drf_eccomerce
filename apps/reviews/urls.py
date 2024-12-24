from django.urls import path

from apps.reviews.views import ReviewsAPIView, SingleReviewAPIView

urlpatterns = [
    path('<slug:product_slug>/', ReviewsAPIView.as_view()),
    path('single_review/<str:review_id>/', SingleReviewAPIView.as_view())
]
