from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# fmt: off
urlpatterns = [
    # 기본 경로
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    # Admin
    path("admin/",admin.site.urls),
    # Swagger-UI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # USER
    path("api/users/", include("users.urls")),
    # FTI
    path("api/ftitests/", include("test_info.fti_urls",)),
    # Taste
    path("api/tastes/", include("test_info.taste_urls")),
    # Profile
    path("api/profile/", include("profiles.urls")),
    # Category
    path("api/categories/", include("categories.urls")),
    # Meeting
    path("api/meetings/", include("meetings.urls")),
    # Review
    path("api/reviews/", include("reviews.urls")),
    # Comment
    path("api/comments/", include("comments.urls")),
    # FoodRecommend
    path("api/foods/", include("foods.urls")),
    # Common Images
    path("api/common/", include("common.urls")),
    # Likes
    path("api/likes/", include("likes.urls")),
]
# fmt: on
