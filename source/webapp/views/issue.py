from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from webapp.views.base import SearchView
from webapp.models import Issue, Project
from webapp.forms import IssueForm, SimpleSearchForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView


class IssuesView(SearchView):
    template_name = 'issue/index.html'
    context_object_name = 'issue_list'
    model = Issue
    paginate_by = 5
    paginate_orphans = 0
    form = SimpleSearchForm
    context = 'query'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset


class IssueView(DetailView):
    template_name = 'issue/view.html'
    model = Issue


class IssueDeleteView(DeleteView):
    model = Issue
    template_name = 'issue/delete.html'
    context_object_name = 'issue'

    def get_success_url(self):
        return reverse("project_view", kwargs={'pk': self.object.project.pk})


def multi_delete_issue(request):
    data = request.POST.getlist('id')
    Issue.objects.filter(pk__in=data).delete()
    return redirect('index')


class IssueCreateView(CreateView):
    model = Issue
    template_name = 'issue/create.html'
    form_class = IssueForm

    def form_valid(self, form):
        project = get_object_or_404(
            Project,
            pk=self.kwargs.get('pk'),
        )
        issue = form.save(commit=False)
        issue.project = project
        issue.save()
        form.save_m2m()
        return redirect('project_view', pk=project.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(
            Project,
            pk=self.kwargs.get('pk'),
        )
        return context


class IssueUpdateView(UpdateView):
    template_name = 'issue/update.html'
    form_class = IssueForm
    model = Issue
    context_object_name = 'issue'

    def get_success_url(self):
        return reverse('issue_view', kwargs={'pk': self.object.pk})
