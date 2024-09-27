from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import re_path
# from monitor.models import LoginMonitor
# from monitor.import_custom import ImportCustom
from .models import *

# @admin.register(admin.ModelAdmin)
# class LoginMonitorAdmin(admin.ModelAdmin):
#     change_list_template = "admin/monitor_change_list.html"
    
    # def get_urls(self):
    #     urls = super(LoginMonitorAdmin, self).get_urls()
    #     custom_urls = [
    #     re_path('^import/$', self.process_import, name='process_import'),]
    #     return custom_urls + urls
    
    # def process_import_btmp(self, request):
    #     import_custom = ImportCustom()
    #     count = import_custom.import_data()
    #     self.message_user(request, f"создано {count} новых записей")
    #     return HttpResponseRedirect("../")

VIEW_ALL = 1
TEACHER = 1
METODIST = 0
URIST = 0
AUTO = 0


if URIST or VIEW_ALL:
    # Учитель
    @admin.register(TeacherProfile)
    class TeacherProfileAdmin(admin.ModelAdmin):
        list_display = ('name1', 'name2', 'name3',)
        
        
    # Учитель-предметы
    @admin.register(Teacher_Subjects)
    class Teacher_SubjectsAdmin(admin.ModelAdmin):
        list_display = ('teacher', 'nclass', 'subject',)
        # change_list_template = "admin\\change_list.html"
    
    

if METODIST or VIEW_ALL:
    # Класс
    @admin.register(nClass)
    class nClassAdmin(admin.ModelAdmin):
        list_display = ('title', 'size', )
        
        
    # Специализация
    @admin.register(Specialization)
    class SpecializationAdmin(admin.ModelAdmin):
        list_display = ('title',  )
        
        
    # Кабинеты
    @admin.register(Room)
    class RoomAdmin(admin.ModelAdmin):
        list_display = ('numb', 'Специализация', )
        
        def Специализация(self, obj):
            spec = obj.spec.all()
            list = []
            for i in spec:
                list.append(i.title)
                
            if list:
                s = list.pop()
                for i in list:
                    s += f", {i}"
            else:
                s = "Пусто"
            # return obj.course.first()
            return s
        
        
    # Предметы
    @admin.register(Subjects)
    class SubjectsAdmin(admin.ModelAdmin):
        list_display = ('title',  )
        
        
    # # Курсы
    # @admin.register(Corse)
    # class DishwasherAdmin(admin.ModelAdmin):
    #     list_display = ('title',  )
        
        
    # Предметы курсов — -
    @admin.register(TrainingCalendar)
    class TrainingCalendarAdmin(admin.ModelAdmin):
        list_display = ('subj', 'time_total', )
        
        def courses(self, obj):
            corses = obj.course.all()
            list = []
            for i in corses:
                list.append(i.title)
                
            s = list.pop()
            for i in list:
                s += f", {i}"
            # return obj.course.first()
            return s
        
        
    # Номера уроков
    @admin.register(LessonNumber)
    class LessonNumberAdmin(admin.ModelAdmin):
        list_display = ('number', 'time_start', 'time_end')
        
        
    # Типы пожеланий
    @admin.register(TypeOfRequest)
    class TypeOfRequestAdmin(admin.ModelAdmin):
        list_display = ('title', )
        
        
    # # Типы работ
    # @admin.register(TypeOfWork)
    # class DishwasherAdmin(admin.ModelAdmin):
    #     list_display = ('title', )
        
        
        
if TEACHER or VIEW_ALL:
    # Блоки расписания
    @admin.register(Blok_timetable)
    class Blok_timetableAdmin(admin.ModelAdmin):
        list_display = ('nclass', 'n_week', 'lesson_number', 'subject', 'room', 'teacher', )
        list_filter = ('nclass', 'n_week', 'subject', 'teacher', )
        # change_list_template = "timetable\\templates\\admin\\change_list.html"
        # change_list_template = "admin/change_list.html"
        # change_list_template = "admin/change_list_filter_sidebar.html"
        # change_list_template = "admin/change_list_filter_confirm_sidebar.html" 
        '''
        То что выше не удалать, нужно для grappelli
        (В settings закоменчено)
        Сейчас доп кнопки не вылетают, так что до того как это профиксится - оставить для быстого
        возвращения
        '''
        
        
    # Пожелания
    @admin.register(TeacherRequests)
    class TeacherRequestsAdmin(admin.ModelAdmin):
        list_display = ('time', 'type',)
        
        
    # # Журнал
    # @admin.register(Jurnal)
    # class DishwasherAdmin(admin.ModelAdmin):
    #     list_display = ('Класс', 'Время', 'Предмет', )
        
    #     def Класс(self, obj):
    #         return obj.timetable.nclass
        
    #     def Время(self, obj):
    #         return obj.timetable.lesson_number
        
    #     def Предмет(self, obj):
    #         return obj.timetable.subject
        
        
    # # Оценки
    # @admin.register(Results)
    # class DishwasherAdmin(admin.ModelAdmin):
    #     list_display = ('Предмет', 'student', 'point', )
        
        
    #     def Предмет(self, obj):
    #         return obj.jurnal.timetable.blok_lesson.subject



if AUTO or VIEW_ALL:
    # Блоки времени
    @admin.register(Blok_time)
    class Blok_timeAdmin(admin.ModelAdmin):
        list_display = ('lesson_number', 'n_week', )
        
        
    # # Блоки занятий
    # @admin.register(Blok_lesson)
    # class DishwasherAdmin(admin.ModelAdmin):
    #     list_display = ('nclass', 'subject', 'teacher', )
        


    
admin.site.site_header = 'Административаня панель'



# admin.site.register(TeacherProfile)
# admin.site.register(nClass)
# admin.site.register(Specialization)
# admin.site.register(Room)
# admin.site.register(Subjects)
# admin.site.register(Teacher_Subjects)
# admin.site.register(Corse)
# admin.site.register(CourseLesson)
# admin.site.register(LessonNumber)
# admin.site.register(Blok_time)

# admin.site.register(Blok_lesson)
# admin.site.register(Blok_timetable)
# admin.site.register(TypeOfRequest)
# admin.site.register(TeacherRequests)
# admin.site.register(Jurnal)
# admin.site.register(TypeOfWork)
# admin.site.register(Results)