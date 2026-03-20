from django.urls import path

from apps.moment.views import CreateMomentView, ListSelfMomentView, ListPublicMomentView, HomeMomentView, \
    DetailMomentView

app_name = 'moment'

urlpatterns = [
    path("", HomeMomentView.as_view(), name="home"),
    path("moments/create/", CreateMomentView.as_view(), name="create"),
    path("moments/public/", ListPublicMomentView.as_view(), name="public_moments_list"),
    path("moments/my/", ListSelfMomentView.as_view(), name="self_moments_list"),
    path("moments/detail/<id>/", DetailMomentView.as_view(), name="detail_moment"),
]
