from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class Department(models.Model):
    class DepartmentName(models.TextChoices):
        ENGINEERING = "engineering" , "Engineering"
        HR = "hr" , "Hr"
        FINANCE = "finance" , "Finance"

    class Departmentcode(models.TextChoices):
        ENG = "eng" , "Eng"
        HR = "hr" , "Hr"
        FIN = "fin" , "Fin"

    name = models.CharField(max_length=50 , choices=DepartmentName.choices , unique=True)
    code = models.CharField(max_length=3 , choices=Departmentcode.choices , unique=True)
    description = models.CharField(max_length=255 , blank=True)
    manager = models.ForeignKey("User" , on_delete=models.SET_NULL , null=True , blank=True , related_name="managed_department")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    class Role(models.TextChoices):
        EMPLOYEE = "employee" , "Employee"
        MANAGER = "manager" , "Manager"
        FINANCE_MANAGER = "finance_manager" , "Finance_manager"
        ADMIN = "admin" , "Admin"

    email = models.EmailField(unique=True)
    employee_id = models.CharField(max_length=28 , unique=True)
    department = models.ForeignKey(to=Department , on_delete=models.PROTECT , null=True , blank=True , related_name="employees")
    manager = models.ForeignKey("self" , on_delete=models.SET_NULL , null=True , blank=True , related_name="employees_managed")
    role = models.CharField(max_length=20 , choices=Role.choices , default=Role.EMPLOYEE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    def __str__(self):
        return self.email

