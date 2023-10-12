from django.urls import path

from . import views

app_name = "Apps.projects"
urlpatterns = [
      path('', views.ProjectsListView, name='projects_list'),
      path('add', views.ProjectsAddView, name='projects_add'),
      path('delete/<str:project_id>',
            views.ProjectsDeleteView, name='projects_delete'),
      path('update/<str:project_id>',
            views.ProjectsUpdateView, name='projects_update'),      
]
