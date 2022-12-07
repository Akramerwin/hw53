from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import MultipleObjectMixin
from webapp.models import Todo, Projects
from webapp.forms import TodoForm, SimpleSearchForm, ProjectsForm
from django.utils.http import urlencode
from django.http import HttpResponseRedirect
from django.views.generic import FormView, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.db.models import Q


class DeleteProjject(DeleteView):
    template_name = 'projects/delete_p.html'
    model = Projects
    context_object_name = 'projects'
    success_url = reverse_lazy('projects')

class UpdateProject(UpdateView):
    model = Projects
    template_name = 'projects/pupdate.html'
    form_class = ProjectsForm
    context_object_name = 'projects'

    def get_success_url(self):
        return reverse('view_p', kwargs={'pk': self.object.pk})

class ProjectsCreate(CreateView):
    template_name = 'projects/pcreate.html'
    model = Projects
    form_class = ProjectsForm

class ProjectsList(ListView):
    template_name = 'projects/ip.html'
    context_object_name = 'projects'
    model = Projects
    ordering = ['-s_date']


class ProjectsView(DetailView):
    template_name = 'projects/view_projects.html'
    model = Projects



class TodoView(ListView):
    template_name = 'todo/index.html'
    context_object_name = 'todo'
    model = Todo
    ordering = ['-date_of_update']
    paginate_by = 10


    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(short_description__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
         context['query'] = urlencode({'search': self.search_value})
         context['search'] = self.search_value
        return context

class View(DetailView):
   template_name = 'todo/todo_view.html'
   model = Todo


class TodoCreate(CreateView):
    template_name = 'todo/todo_create.html'
    model = Todo
    form_class = TodoForm

    def form_valid(self, form):
        projects = get_object_or_404(Projects, pk=self.kwargs.get('pk'))
        print(projects)
        form.instance.p_id = projects
        return super().form_valid(form)

class UpdateTodo(UpdateView):
    template_name = 'todo/todo_update.html'
    form_class = TodoForm
    model = Todo
    context_object_name = 'todo'


class Delete(DeleteView):
    template_name = 'todo/delete.html'
    model = Todo
    context_object_name = 'todo'
    success_url = reverse_lazy('index')

