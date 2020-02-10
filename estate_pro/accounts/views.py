from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import OuterRef, Subquery, Q

from . import forms
from . import models
from estate_app import models as estate_models
from estate_app import forms as estate_forms

class AuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != self.request.user:
            return redirect('estate_app:my_offers_list')
        return super().dispatch(request, *args, **kwargs)

class SignUp(CreateView):

    form_class = forms.UserSignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form, formset):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('accounts:login')

    def form_invalid(self, form, formset):
        return render(self.get_context_data(form=form, formset=formset, template_name = 'accounts/login.html'))

    def get(self, *args, **kwargs):
        self.object = None
        form_class = forms.UserSignUpForm
        form = self.get_form(form_class)

        formset = forms.UserDetailsFormSet(queryset=models.UserDetails.objects.none())

        template_name = 'accounts/signup.html'
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = forms.UserDetailsFormSet(self.request.POST or None)

        if (form.is_valid() and formset.is_valid()):
            self.object = form.save()
            for f in formset:
                # details = models.UserDetails(
                #     user = self.object,
                #     phone_num = f.cleaned_data['phone_num'],
                #     name = f.cleaned_data['name'])
                details = f.save(commit=False)
                details.user = self.object
                details.save()

            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

class UserDetailsView(DetailView):

    model = models.UserDetails
    template_name = 'accounts/user_details.html'

class DetailsUpdate(AuthorRequiredMixin, UpdateView):
    fields = ('phone_num', 'name')
    model = models.UserDetails
    template_name = 'accounts/details_edit.html'

    def get_success_url(self):
     return reverse_lazy('estate_app:my_offers_list')

class ChatReplyView(LoginRequiredMixin, CreateView):

    model = estate_models.UserMessages
    template_name = 'accounts/chat_reply.html'
    fields = ('title', 'message')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = estate_models.UserMessages.objects.filter(
            msg_receiver = self.request.user, msg_sender = self.kwargs['pk'])

        for msg in messages:
            if msg.is_read == False:
                estate_models.UserMessages.objects.get(
                id = msg.id).read_msg()

        context['form'] = self.get_form(estate_forms.MessagesForm)
        context['usermessages_list'] = estate_models.UserMessages.objects.filter((
            (Q(msg_receiver = self.request.user) & Q(msg_sender = self.kwargs['pk']))
            | (Q(msg_receiver = self.kwargs['pk']) & Q(msg_sender = self.request.user)))).order_by('-pk')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.msg_sender = self.request.user
        self.object.msg_receiver = User.objects.get(id = self.kwargs['pk'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        propertyid = self.kwargs['pk']
        return reverse_lazy('accounts:chat_details', kwargs={'pk': propertyid})

class InboxChatView(LoginRequiredMixin, ListView):

    model = estate_models.UserMessages
    template_name = 'accounts/Chat_list.html'

    def get_queryset(self):
        subq = estate_models.UserMessages.objects.filter(
            msg_receiver = self.request.user.id, msg_sender = OuterRef('msg_sender')).order_by('-id')
        final = estate_models.UserMessages.objects.filter(pk=Subquery(subq.values('pk')[:1]))
        return final.order_by('-id')

# class UserChatView(LoginRequiredMixin, ListView):
#
#     model = estate_models.UserMessages
#     template_name = 'accounts/chat_details.html'
#
#     def get_queryset(self):
#         messages = estate_models.UserMessages.objects.filter(
#             msg_receiver = self.request.user, msg_sender = self.kwargs['pk'])
#         for msg in messages:
#             if msg.is_read == False:
#                 estate_models.UserMessages.objects.get(
#                 id = msg.id).read_msg()
#
#         qs = estate_models.UserMessages.objects.filter((
#             (Q(msg_receiver = self.request.user) & Q(msg_sender = self.kwargs['pk']))
#             | (Q(msg_receiver = self.kwargs['pk']) & Q(msg_sender = self.request.user)))).order_by('-pk')
#         return qs

# class UserMessagesView(LoginRequiredMixin, ListView):
#
#     model = estate_models.UserMessages
#     template_name = 'accounts/inbox.html'
#
#     def get_queryset(self):
#         return estate_models.UserMessages.objects.filter(msg_receiver = self.request.user)

# class UserMessagesView(LoginRequiredMixin, ListView):
#
#     model = estate_models.UserMessages
#     template_name = 'accounts/inbox.html'
#
#     def get_queryset(self):
#         return estate_models.UserMessages.objects.filter(msg_receiver = self.request.user)

# class MessageDetailsView(LoginRequiredMixin, DetailView):
#
#     model = estate_models.UserMessages
#     template_name = 'accounts/messages.html'
#
#     def get_queryset(self):
#         estate_models.UserMessages.objects.fi(id = self.kwargs['pk']).read_msg()
#         return estate_models.UserMessages.objects.filter(id = self.kwargs['pk'])
