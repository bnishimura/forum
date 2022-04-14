from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(View):
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        return render(request, 'signup.html', { form=form })
