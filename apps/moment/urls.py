from django.urls import path

from apps.moment.views import CreateMomentView

app_name = 'moment'

urlpatterns = [
    path("create/", CreateMomentView.as_view(), name="create")
]