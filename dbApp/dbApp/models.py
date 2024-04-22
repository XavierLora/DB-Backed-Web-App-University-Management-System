from django.db import models

class Instructor(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=32)
    dept_name = models.CharField(max_length=32)
    salary = models.IntegerField()
    class Meta:
        db_table = 'instructor'

class Teaches(models.Model):
    course_id = models.CharField(max_length=8)
    sec_id = models.CharField(max_length=4)
    semester = models.IntegerField()
    year = models.IntegerField()
    teacher_id = models.CharField(max_length=5)
    class Meta:
        db_table = 'teaches'
        unique_together = ('course_id', 'sec_id', 'semester', 'year', 'teacher_id')

class Takes(models.Model):
    student_id = models.CharField(max_length=8)
    course_id = models.CharField(max_length=8)
    sec_id = models.CharField(max_length=4)
    semester = models.IntegerField()
    year = models.IntegerField()
    grade = models.CharField(max_length=2)
    class Meta:
        db_table = 'takes'
        unique_together = ('student_id', 'course_id', 'sec_id', 'semester', 'year')

class Students(models.Model):
    student_id = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=32)
    dept_name = models.CharField(max_length=32)
    total_credit = models.IntegerField()
    class Meta:
        db_table = 'student'
    