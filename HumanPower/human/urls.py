from django.conf.urls  import url   
from human import views 

app_name = 'human'
  
urlpatterns = [  
    # index
    url(r'^$', views.HumanFormView.as_view(), name='index'),  

    # account
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^register/$', views.register, name='register'),

    # case
    url(r'^cases/$', views.CaseList.as_view(), name='case-list'),  
    url(r'^cases/(?P<pk>[0-9]+)/$', views.CaseDetail.as_view(), name='case-detail'),  
    url(r'^cases/(?P<pk>[0-9]+)/items/(?P<pk2>[0-9]+)/submit/$', views.ItemHumanCreate.as_view(), name='itemhuman-create'),
    
    # items
    url(r'^items/$', views.ItemHumanList.as_view(), name='itemhuman-list'),
    url(r'^items/(?P<pk>[0-9]+)/$', views.ItemHumanUpdate.as_view(), name='itemhuman-update'),
    url(r'^items/(?P<pk>[0-9]+)/action/$', views.ItemHumanAction.as_view(), name='itemhuman-action'),
]  