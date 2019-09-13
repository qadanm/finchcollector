from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Finch, Toy
from .forms import FeedingForm

# View functions

def signup(request):
    error_message = ''
    if request.method == 'POST':
      # This is how to create a 'user' form object
      # that includes the data from the browser
      form = UserCreationForm(request.POST)
      if form.is_valid():
          # This will add the user to the database
          user = form.save()
          # This is how we log a user in via code
          login(request, user)
          return redirect('index')
      else:
          error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def finches_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', { 'finches': finches })


@login_required
def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    toys_finch_doesnt_have = Toy.objects.exclude(id__in = finch.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'finches/detail.html',
     {'finch': finch,
      'feeding_form': feeding_form,
      'toys': toys_finch_doesnt_have
    })


class FinchCreate(LoginRequiredMixin, CreateView):
    model = Finch
    fields = ['name', 'breed', 'description', 'age']
  # This inherited method is called when a
  # valid cat form is being submitted
    def form_valid(self, form):
  # Assign the logged in user (self.request.user)
      form.instance.user = self.request.user
  # Let the CreateView do its job as usual
      return super().form_valid(form)

class FinchUpdate(LoginRequiredMixin, UpdateView):
    model = Finch
    fields = ['breed', 'description', 'age']

class FinchDelete(LoginRequiredMixin, DeleteView):
    model = Finch
    success_url = '/finches/'

@login_required
def add_feeding(request, finch_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('detail', finch_id=finch_id)

class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'


@login_required
def assoc_toy(request, finch_id, toy_id):
  Finch.objects.get(id=finch_id).toys.add(toy_id)
  return redirect('detail', finch_id=finch_id)
