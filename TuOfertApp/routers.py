from users.views import *

from business.views import *

from rest_framework import routers

router = routers.DefaultRouter()
# User App
router.register(r'cliente', UserClientViewset)

# Business App
router.register(r'business', BusinessViewset)
router.register(r'oferts', OfertsViewset)