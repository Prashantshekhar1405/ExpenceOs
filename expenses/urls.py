from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet , ExpenseCategoryViewSet

router = DefaultRouter()

router.register("expenses",ExpenseViewSet ,basename="expense")
router.register("categories", ExpenseCategoryViewSet, basename="category")

urlpatterns = router.urls
