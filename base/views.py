from django.shortcuts import render,redirect
from django.views.generic.list import ListView
#detail information about items
from django.views.generic.detail import DetailView
#for create view
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from .models import Task
#redirect users to cetain page
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
#once user registrated user has to login automatically 
from django.contrib.auth import login

#permission to view and edit
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView,LogoutView



# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    #function to take to login page once valid form is submitted
    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    
    #if user is aunthenicated dont show register page
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage,self).get(*args,**kwargs)





class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    

    #over riding get_context_data method to only show tasks of logged in user
    def get_context_data(self, **kwargs):
        #making sure we were inherting from original method
        context = super().get_context_data(**kwargs)
        #only show tasks of logged in user
        context['tasks'] = context['tasks'].filter(user=self.request.user) 
        context['count'] = context['tasks'].filter(complete=False).count()
        #to get search input
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__contains=search_input)

        context['search_input'] = search_input
        return context
    

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_detail.html'


class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

    #for overriding the default form
    #only logged in user can create task in his name
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)



class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields =['title','description','complete']
    success_url = reverse_lazy('tasks')



class DeleteTask(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

    


    
