from rest_framework.routers import DefaultRouter
from .views import ReimbursementViewSet

router = DefaultRouter()

router.register("reimbursements" , ReimbursementViewSet , basename="reimbursement")

urlpatterns = router.urls
