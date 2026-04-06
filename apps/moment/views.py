from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.moment.forms import MomentForm
from apps.moment.models import Moment


class CreateMomentView(LoginRequiredMixin, CreateView):
    """Контролер для создания момента"""

    form_class = MomentForm
    template_name = "moment/moment_form.html"
    success_url = reverse_lazy("moment:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submit_label"] = "Сохранить момент"
        context["title"] = "Создать момент"
        return context

    def post(self, request, *args, **kwargs):
        print("FILES:", request.FILES)
        return super().post(request, *args, **kwargs)


class HomeMomentView(ListView):
    """Контролер для главной страницы"""

    form_class = MomentForm
    template_name = "moment/moment_home.html"
    context_object_name = "moments"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Moment.objects.filter(owner=self.request.user).order_by(
                "-created_at"
            )
        return Moment.objects.filter(is_public=True).order_by("-created_at")


class ListSelfMomentView(LoginRequiredMixin, ListView):
    """Контролер для вывода списка своих моментов"""

    form_class = MomentForm
    template_name = "moment/self_moment_list.html"
    context_object_name = "moments"
    paginate_by = 10

    def get_queryset(self):
        queryset = Moment.objects.filter(owner=self.request.user).order_by("-created_at")

        period = self.request.GET.get("period")

        if period:
            year, month = period.split("-")
            queryset = queryset.filter(
                created_at__year=year,
                created_at__month=month
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["periods"] = (
            Moment.objects.filter(owner=self.request.user)
            .dates("created_at", "month", order="DESC")
        )
        context["selected_period"] = self.request.GET.get("period", "")

        return context


class ListPublicMomentView(ListView):
    """Контролер для вывода списка своих моментов"""

    form_class = MomentForm
    template_name = "moment/public_moment_list.html"
    context_object_name = "moments"
    paginate_by = 10

    def get_queryset(self):
        return Moment.objects.filter(is_public=True).order_by("-created_at")


class SearchMomentView(ListView):
    form_class = MomentForm
    template_name = "moment/moment_search.html"
    context_object_name = "moments"

    def get_queryset(self):
        return Moment.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()

        my_results = Moment.objects.none()
        public_results = Moment.objects.none()

        if query:
            search_q = Q(title__icontains=query) | Q(details__icontains=query)

            if self.request.user.is_authenticated:
                my_results = Moment.objects.filter(
                    owner=self.request.user
                ).filter(search_q)

                public_results = Moment.objects.filter(
                    is_public=True
                ).exclude(
                    owner=self.request.user
                ).filter(search_q)
            else:
                public_results = Moment.objects.filter(
                    is_public=True
                ).filter(search_q)

        context["query"] = query
        context["my_results"] = my_results
        context["public_results"] = public_results
        return context


class DetailMomentView(LoginRequiredMixin, DetailView):
    form_class = MomentForm
    template_name = "moment/moment_detail.html"
    context_object_name = "moment"

    def get_queryset(self):
        return Moment.objects.filter(Q(owner=self.request.user) | Q(is_public=True))


class UpdateMomentView(LoginRequiredMixin, UpdateView):
    form_class = MomentForm
    template_name = "moment/moment_form.html"

    def get_queryset(self):
        return Moment.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy("moment:moment_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submit_label"] = "Сохранить изменения"
        context["title"] = "Редактировать момент"
        return context


class DeleteMomentView(LoginRequiredMixin, DeleteView):
    model = Moment
    template_name = "moment/moment_confirm_delete.html"
    context_object_name = "moment"
    success_url = reverse_lazy("moment:home")

    def get_queryset(self):
        return Moment.objects.filter(owner=self.request.user)
