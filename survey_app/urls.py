"""microphone_medical_survey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='survey_list'),
    path('name', views.get_name),
    path('admin/', admin.site.urls),
    path('survey_list/<int:page>',views.survey_list, name='survey_list'),
    path('survey_creator',views.survey_creator, name='survey_creator'),
    path('survey_creator/<int:survey_id>/<int:page>',views.survey_creator, name='survey_creator'),
    path('survey/<int:survey_id>/<int:survey_page>', views.survey_page, name='survey_page'),
    path('survey/delete_survey', views.delete_survey, name='delete_survey'),
    path('survey/delete_question', views.delete_question, name='delete_survey'),

]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
