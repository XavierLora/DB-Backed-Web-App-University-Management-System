from django.db import models

class Instructor(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=32)
    dept_name = models.CharField(max_length=32)
    salary = models.IntegerField()
    class Meta:
        db_table = 'instructor'

class Teaches(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.CharField(max_length=8)
    sec_id = models.CharField(max_length=4)
    semester = models.IntegerField()
    year = models.IntegerField()
    teacher_id = models.CharField(max_length=5)
    class Meta:
        db_table = 'teaches'

class Takes(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.CharField(max_length=8)
    course_id = models.CharField(max_length=8)
    sec_id = models.CharField(max_length=4)
    semester = models.IntegerField()
    year = models.IntegerField()
    grade = models.CharField(max_length=2)
    class Meta:
        db_table = 'takes'
# class Course(models.Model):
    