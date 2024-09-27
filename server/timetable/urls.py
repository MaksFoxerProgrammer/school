from django.urls import path
from timetable import views


# urlpatterns = [
#     path('', views.MainView.as_view(), name="home"),
    
#     path('add-test-rooms/', views.add_rooms, name="t_rooms"),
#     path('add-test-subjects/', views.add_subjects, name="t_subjects"),
#     path('add-test-classes/', views.add_classes, name="t_classes"),
#     path('add-test-students/', views.add_students, name="t_students"),
#     path('add-test-teachers/', views.add_teachers, name="t_teachers"),
#     path('add-test-organization/', views.add_organization, name="t_org"),
#     path('add-test-data/', views.add_data, name="t_data"),
    
#     path('see/', views.SeeDbView.as_view(), name="view-db"),
#     # path('see/<str:s>', views.DBViewer.as_view(), name="view-db"),
    
#     # path('see-sub/<int:pk>/', views.ViewSubjects.as_view(), name="view-sub-int"),
    
#     path('see/students/', views.ListStudents.as_view(), name=""),
#     path('see/classes/', views.ListClasses.as_view(), name=""),
    
#     path('see/teachers/', views.ListTeachers.as_view(), name=""),
#     path('see/rooms/', views.ListRooms.as_view(), name=""),
#     path('see/sub/', views.ListSub.as_view(), name="view-sub"),
#     path('see/organizations/', views.ListOrg.as_view(), name=""),
#     path('see/users/', views.ListUsers.as_view(), name=""),
    
#     path('create/TrainingCalendar/', views.CreateTrainingCalendar.as_view(), 
#          name="TrainingCalendar"),
# ]

urlpatterns = [
    path('test_data/', views.geterate_test_data, name="test_data"),
    path('data/', views.add_real_data, name="data"),    
    path('del_data/', views.delete_everything, name="del_data"),    
    
    
    
    
    path('admin/timetable/blok_timetable/createTimeTable/', views.createTimeTable, 
         name="t_createTimeTable"),
    
    path('', views.main_page, name="home"),
]