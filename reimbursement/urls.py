from rest_framework.routers import DefaultRouter
from .views import ReimbursementViewSet

router = DefaultRouter()

router.register("reibursements" , ReimbursementViewSet , basename="reimbursement")

urlpatterns = router.urls
