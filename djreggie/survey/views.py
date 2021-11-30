# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from djauth.decorators import portal_auth_required
from djreggie.survey.forms import OnlineCourseForm
from djreggie.survey.sql import INSERT_CTC_REC
from djzbar.utils.informix import do_sql


DEBUG=settings.INFORMIX_DEBUG
EARL=settings.INFORMIX_EARL


@portal_auth_required(
    session_var='DJREGGIE_AUTH', redirect_url=reverse_lazy('access_denied'),
)
def courses(request):
    """Data integrity and error handling, insert data from survey form."""
    user = request.user
    if request.method == 'POST':
        form = OnlineCourseForm(request.POST)
        if form.is_valid():
            # save our data
            data = form.save(commit=False)
            data.created_by = user
            data.updated_by = user
            data.save()
            # insert data into informix
            sql = INSERT_CTC_REC(cid=user.id)
            do_sql(sql, key=DEBUG, earl=EARL)
            return HttpResponseRedirect(reverse_lazy('survey_success'))
    else:
        form = OnlineCourseForm()

    return render(request, 'survey/form.html', {'form': form})
