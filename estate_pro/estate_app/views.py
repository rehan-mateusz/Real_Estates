from django.shortcuts import redirect, render, render_to_response
from django.http import HttpResponseRedirect
from django.views.generic import  DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django_filters.views import BaseFilterView


from . import models
from . import forms
from . import filters

User = get_user_model()

class AuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            return redirect('estate_app:my_offers_list')
        return super(AuthorRequiredMixin, self).dispatch(request, *args, **kwargs)

class PropertyDetailView(CreateView):

    form_class = forms.MessagesForm
    template_name = 'estate_app/propertymodel_detail.html'

    def get_success_url(self):
        propertyid = self.kwargs['pk']
        return reverse_lazy('estate_app:property_detail_view', kwargs={'pk': propertyid})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['propertymodel'] = models.PropertyModel.objects.get(id = self.kwargs['pk'])
        context['form'] = self.get_form(forms.MessagesForm)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.msg_sender = self.request.user
        self.object.msg_receiver = models.PropertyModel.objects.get(id = self.kwargs['pk']).author
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class PropertyListView(BaseFilterView, ListView):

    model = models.PropertyModel
    paginate_by = 1
    filterset_class = filters.PropertyFilter

class PropertyCreateView(LoginRequiredMixin, CreateView):

    fields = ('title', 'text', 'price', 'city', 'estate_type')
    model = models.PropertyModel
    template_name = 'estate_app/property_create_form.html'

    def form_valid(self, form, formset):
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        print( formset)
        if form.is_valid() == False:
            print("FORM INVALID")
        if formset.is_valid() == False:
            print("FORMSET INVALID")
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_success_url(self):
        return reverse_lazy('estate_app:my_offers_list')

    def get(self, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = forms.ImagesCreateFormSet(queryset=models.ImagesModel.objects.none())
        template_name = 'estate_app/property_create_form.html'
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = forms.ImagesCreateFormSet(self.request.POST, self.request.FILES or None)
        if (form.is_valid() and formset.is_valid()):
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.save()
            for img in formset:
                try:
                    photo = models.ImagesModel(property = self.object, image = img.cleaned_data['image'])
                    photo.save()
                except Exception as e:
                    pass
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

class PropertyEditView(AuthorRequiredMixin, LoginRequiredMixin,  UpdateView):
    fields = ('title', 'text', 'price', 'city', 'estate_type')
    model = models.PropertyModel
    template_name = 'estate_app/propertymodel_edit.html'

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = forms.ImagesCreateFormSet(instance = self.object)
        return self.render_to_response(self.get_context_data(form = form, formset = formset))

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = forms.ImagesCreateFormSet(self.request.POST, self.request.FILES, instance=self.object)

        if (form.is_valid() and formset.is_valid()):
            self.object = form.save()
            for img in formset:

                try:
                    if not img.instance.pk:
                        photo = models.ImagesModel(property = self.object, image = img.cleaned_data['image'])
                        photo.save()

                    elif img.cleaned_data['DELETE']:
                        photo = models.ImagesModel.objects.get(pk = img.instance.id)
                        photo.delete()

                    else:
                        photo = models.ImagesModel.objects.get(pk = img.instance.id)
                        photo.image = img.cleaned_data['image']
                        photo.save()

                except Exception as e:
                    pass

            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form = form, formset = formset))

    def form_valid(self, form, formset):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        propertyid = self.kwargs['pk']
        return reverse_lazy('estate_app:property_detail_view', kwargs={'pk': propertyid})

class PropertyDeleteView(AuthorRequiredMixin, LoginRequiredMixin, DeleteView):
    model = models.PropertyModel
    template_name = 'estate_app/delete_property.html'

    def get_success_url(self):
        return reverse_lazy('estate_app:my_offers_list')

class MyOfferList(LoginRequiredMixin, BaseFilterView, ListView):

    model = models.PropertyModel
    template_name = 'estate_app/my_offers_list.html'
    paginate_by = 1
    filterset_class = filters.PropertyFilter

    def get_queryset(self):
        return models.PropertyModel.objects.filter(author=self.request.user).order_by('-id')

class UserOffersList(BaseFilterView, ListView):

    model = models.PropertyModel
    template_name = 'estate_app/user_offers_list.html'
    paginate_by = 1
    filterset_class = filters.PropertyFilter

    def get_queryset(self):
        return models.PropertyModel.objects.filter(author = User.objects.get(username = self.kwargs['username'])).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_author'] = self.kwargs['username']
        return context
