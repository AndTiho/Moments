from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from apps.moment.forms import MomentForm
from apps.moment.models import Moment


class CreateMomentView(LoginRequiredMixin, CreateView):
    model = Moment
    form_class = MomentForm
    template_name = "moment/moment_form.html"
    success_url = reverse_lazy("moment:create")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class HomeMomentView(ListView):
    model = Moment
    template_name = "moment/moment_home.html"
    context_object_name = "moments"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Moment.objects.filter(
                owner=self.request.user
            ).order_by("-created_at")
        return Moment.objects.filter(
            is_public=True
        ).order_by("-created_at")

class ListSelfMomentView(LoginRequiredMixin, ListView):
    model = Moment
    template_name = "moment/self_moment_list.html"
    context_object_name = "moments"
    paginate_by = 10

    def get_queryset(self):
        return Moment.objects.filter(
            owner=self.request.user
        ).order_by("-created_at")

class ListPublicMomentView(ListView):
    model = Moment
    template_name = "moment/public_moment_list.html"
    context_object_name = "moments"
    paginate_by = 10

    def get_queryset(self):
        return Moment.objects.filter(
            is_public=True
        ).order_by("-created_at")

class DetailMomentView(LoginRequiredMixin, DetailView):
    model = Moment
    template_name = "moment/moment_detail.html"
    context_object_name = "moment"

