from django.contrib import admin
# from django.contrib.admin.decorators import display

from .models import *


@admin.register(Timetable)
class Timetable(admin.ModelAdmin):
    list_display = ('clas', 'subj', 'd', 'm', 'y',)
    list_display_links = ("clas", 'subj')
    search_fields = ('clas', 'subj')
    list_filter = ('clas', 'subj')
    save_on_top = True
    fieldsets = (
        ("Основное", {
            "fields": (("numb", "d", "m", "y"), ("clas", "subj", "room",), ("teacher", "org",),)
        }),
    )

    #  fieldsets = (
    #     ("Главные", {
    #         "fields": (("title", "img", "currency"), ("price", "square", "floor"))
    #     }),
    #     ('Адрес', {
    #         'classes': ('collapse',),
    #         'fields': (('city', "country", "district"), ('full', ), ('lng', 'lat', "zip"))
    #     }),
    #     ("Описание и Правила", {
    #         'classes': ('collapse',),
    #         "fields": ("descriptions", 'rules')
    #     }),
    #     ("Активность", {
    #         "fields": (("is_active", "is_sale", "booking"),)
    #     })


@admin.register(StudentProfile)
class StudentProfile(admin.ModelAdmin):
    list_display = ('user', 'ncls',)
    fieldsets = (
        ("Недоступно для редактирования. (Если доступно, то это для тестов)", {
            # "fields": ()
            "fields": ('user', 'ncls', )
        }),
    )


@admin.register(TeacherProfile)
class TeacherProfile(admin.ModelAdmin):
    list_display = ('user', 'description',)
    list_display_links = (None)
    fieldsets = (
        ("Недоступно для редактирования. (Если доступно, то это для тестов)", {
            # "fields": ()
            "fields": ('user', 'description',)
        }),
    )


admin.site.register(Organization)

admin.site.register(nClass)
admin.site.register(Room)
admin.site.register(Subjects)

# admin.site.register(Timetable, TimetableAdmin)

admin.site.register(TrainingCalendar)
admin.site.register(Specialization)
admin.site.register(Contacts)

# admin.site.register(TeacherProfile)
# admin.site.register(StudentProfile)
