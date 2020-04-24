from django.contrib import admin
from djreggie.survey.models import OnlineCourse


class OnlineCourseAdmin(admin.ModelAdmin):
    model = OnlineCourse
    raw_id_fields = ('created_by', 'updated_by')
    list_max_show_all = 500
    list_per_page = 500
    list_display = (
        'last_name',
        'first_name',
        'email',
        'created_on',
        'course1',
        'course2',
        'course3',
        'course4',
        'course5',
        'course6',
        'course7',
        'course8',
    )
    ordering = (
        '-created_on',
        'created_by__last_name',
        'created_by__first_name',
        'created_by__email',
    )
    search_fields = (
        'course1',
        'course2',
        'course3',
        'course4',
        'course5',
        'course6',
        'course7',
        'course8',
        'created_by__last_name',
        'created_by__username',
    )

admin.site.register(OnlineCourse, OnlineCourseAdmin)
