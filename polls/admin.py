from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    # The following assignment determines the display order of the fields
    # at the admin page
    fields = ['pub_date', 'question_text']


admin.site.register(Question, QuestionAdmin)
