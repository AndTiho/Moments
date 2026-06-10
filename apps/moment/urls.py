from django.urls import path

from apps.moment.views import (CreateMomentView, DeleteMomentView,
                               DetailMomentView, HomeMomentView,
                               ListPublicMomentView, ListSelfMomentView,
                               SearchMomentView, UpdateMomentView)

app_name = "moment"

urlpatterns = [
    path("", HomeMomentView.as_view(), name="home"),
    path("create/", CreateMomentView.as_view(), name="create"),
    path("public/", ListPublicMomentView.as_view(), name="public_moments_list"),
    path("my/", ListSelfMomentView.as_view(), name="self_moments_list"),
    path("detail/<int:pk>/", DetailMomentView.as_view(), name="moment_detail"),
    path("update/<int:pk>/", UpdateMomentView.as_view(), name="moment_update"),
    path("delete/<int:pk>/", DeleteMomentView.as_view(), name="moment_delete"),
    path("search/", SearchMomentView.as_view(), name="search"),
]
