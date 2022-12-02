from django.shortcuts import render, reverse, redirect, get_object_or_404
from webapp.models import Todo
from webapp.forms import TodoForm, SimpleSearchForm
from django.utils.http import urlencode
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView, ListView
from django.db.models import Q


class TodoView(ListView):
    template_name = 'index.html'
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





class View(TemplateView):
   template_name = 'todo_view.html'

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['todo'] = get_object_or_404(Todo, pk=kwargs['pk'])
       return context


class TodoCreate(FormView):
    template_name = 'todo_create.html'
    form_class = TodoForm

    def get_success_url(self):
        return reverse('view', kwargs = {'pk': self.todo.pk})

    def form_valid(self, form):
        self.todo = form.save()
        return super().form_valid(form)


class UpdateTodo(FormView):
    template_name = 'todo_update.html'
    form_class = TodoForm

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Todo, pk = pk)

    def dispatch(self, request, *args, **kwargs):
        self.todo = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo'] = self.todo
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.todo
        return kwargs


    def form_valid(self, form):
        self.todo = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view', kwargs = {'pk': self.todo.pk})



class Delete(View):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        return render(request, 'delete.html', context={'todo': todo})
    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        todo.delete()
        return redirect('index')