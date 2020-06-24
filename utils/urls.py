from .views import *

app_name = 'utils'
urlpatterns = [
    path('utils/token/', HomeTokenView.as_view(), name='home_token'),
    path('api/user/token/', UserTokenDetailView.as_view(), name="current_user_token"),
]
