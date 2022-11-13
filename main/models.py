from django.db import models


class Project(models.Model):
    # Project id
    id = models.CharField(max_length=50, unique=True, primary_key=True)


class Task(models.Model):
    # Task id
    taskid = models.CharField(max_length=50)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    unique_together = ("id", "project")

    # Quantity
    quantity = models.IntegerField()

    # Quantity unit
    qu = models.CharField(max_length=10)

    # Text shortly outlining what the task does
    outline_text = models.CharField(max_length=600)

    # Text precisely detailing what the task does
    detail_text = models.CharField(max_length=1500)

    # Child tasks
    tasks = models.ManyToManyField(to="self", blank=True)

    start = models.DateTimeField(blank=True, null=True, default=None)
    duration = models.IntegerField(blank=True, null=True, default=None)
    estimated = models.BooleanField(default=True)