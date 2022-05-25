
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.forms import IntegerField

def in_upload_path(instance, filename):
    return "/".join(["testcases", str(instance.problem.id)]) + ".in"

def out_upload_path(instance, filename):
    return "/".join(["testcases", str(instance.problem.id)]) + ".out"
# Create your models here.

class Coder(models.Model):
    user = models.CharField(max_length=100)
    link = models.URLField()
    score = models.DecimalField(default=0, decimal_places= 3, max_digits= 100)
    rank = models.IntegerField(default = -1)
    problems_tried = models.IntegerField(null=True, default=0)
    problems_ac = models.IntegerField( null = False, default=0)

    def __unicode__(self):
        return self.user.username

class Problem(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    link = models.URLField()
    statement = models.TextField()

    num_submission = models.IntegerField()
    num_ac = models.IntegerField(default=0)
    num_wa = models.IntegerField(default=0)
    num_re = models.IntegerField(default=0)
    num_tle = models.IntegerField(default=0)
    num_ce = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add= True)
    time_limit = models.IntegerField(default=1)
    source = models.CharField(max_length=200)
    num_tests = models.IntegerField(default=1)
    author =  models.CharField(max_length=50, default="admin")

    def __unicode__(self):
        return self.code
    

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_file = models.FileField(upload_to=in_upload_path)
    output_file = models.FileField(upload_to=out_upload_path)

    def __unicode__(self):
        return self.problem.code
LANGUAGES =(
    ("C", "GNU C"),
    ("CPP", "GNU C++"),
    )

   
class Submission(models.Model):
    STATUSES = (
        ("NT", "Not tested"),
        ("CE", "Compile Error"),
        ("TL", "Time Limit Exceed"),
        ("RE", "Runtime Error"),
        ("AC", "Accepted")
    )
    
    submitter = models.ForeignKey(Coder, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, default="NT", choices= STATUSES)
    lang = models.CharField(max_length= 4, default= "C", choices= LANGUAGES)
    code = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=True)


