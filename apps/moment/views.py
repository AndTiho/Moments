from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

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