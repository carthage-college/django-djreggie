# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from djreggie.survey.forms import OnlineCourseForm
from djzbar.decorators.auth import portal_auth_required


@portal_auth_required(
    session_var='DJREGGIE_AUTH', redirect_url=reverse_lazy('access_denied'),
)
def courses(request):

    user = request.user

    if request.method == 'POST':
        form = OnlineCourseForm(request.POST)
        if form.is_valid():
            # save our data
            data = form.save(commit=False)
            data.created_by = request.user
            data.updated_by = request.user
            data.save()
            return HttpResponseRedirect(reverse_lazy('survey_success'))
    else:
        form = OnlineCourseForm()

    return render(request, 'survey/form.html', {'form': form})
