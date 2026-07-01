from django.db import models

# Create your models here.
from django.db import models

class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateTimeField()
    gender = models.CharField(max_length=6)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField()
    is_delete = models.BooleanField()
    father_name = models.CharField(max_length=100, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    parent_contact_number = models.CharField(max_length=10)
    student_contact_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=500)
    course_pursing = models.CharField(max_length=100)
    address_location = models.CharField(max_length=1000, null=True, blank=True)
    family_source_of_income = models.CharField(max_length=500)
    family_monthly_income = models.DecimalField(max_digits=19, decimal_places=4)
    residential_status = models.CharField(max_length=20)
    additional_assets = models.CharField(max_length=50)
    total_monthly_average_expense_siblings = models.DecimalField(max_digits=19, decimal_places=4)
    family_member_count = models.IntegerField()
    date_of_joining = models.DateTimeField(null=True, blank=True)
    support_type = models.CharField(max_length=20, null=True, blank=True)
    studying_at = models.CharField(max_length=200, null=True, blank=True)
    course_name = models.CharField(max_length=200, null=True, blank=True)
    course_type = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'students'
        managed = False

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}"
