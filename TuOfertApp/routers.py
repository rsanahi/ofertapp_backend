from users.views import *
from rest_framework import routers

router = routers.DefaultRouter()
# User App
router.register(r'cliente', UserClientViewset)