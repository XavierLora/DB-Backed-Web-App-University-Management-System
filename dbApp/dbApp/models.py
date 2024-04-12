from django.db import models

class Instructor(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=32)
    dept_name = models.CharField(max_length=32)
    salary = models.IntegerField()
    class Meta:
        db_table = 'instructor'

class Student(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=32)
    dept_name = models.CharField(max_length=32)
    total_credits = models.IntegerField()
    class Meta:
        db_table = 'student'

# class Course(models.Model):
    