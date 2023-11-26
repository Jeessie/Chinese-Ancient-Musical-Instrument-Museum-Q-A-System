from django.urls import path
from django.urls import include,path
import views

urlpatterns = [
    path('', views.index, name='index'),#首页Home
    path('query/',views.get_detail,name='query'),#用户查询页面
    # 后台管理员登录登出路由
    path('admin/',views.admin,name='login'),
    path('logout/',views.admin_logout,name='logout'),
    # 管理员登录后操作路由
    path('manage/',views.manage,name='add')
]