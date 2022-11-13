from django.shortcuts import render
from .models import *
import datetime
import json
from django.http import HttpResponse
from .classifier import main as run_classification


def index(request):
    return render(request, "index.html")


def main(request, project_id):
    tasks = list(Task.objects.filter(project_id=project_id))


    for i, task in enumerate(tasks):
        if task.start is None:
            task.start = datetime.datetime.now()
        task.end = (task.start + datetime.timedelta(days=task.duration)).strftime("%Y/%m/%d")
        task.start = task.start.strftime("%Y/%m/%d")
        task.outline_text += f" [taskid: {task.taskid}]"

        task.id = i+1


    return render(request, "gantt.html", {"data": tasks})

def save(request):
    tasks = json.loads(request.GET["tasks"])
    taskDurations = json.loads(request.GET["taskDurations"])


    tasks = {i["id"]: [i["name"].split(" [taskid: ")[1].replace("]", ""), i["name"]] for i in tasks}
    taskDurations = {i["task"]: [i["start"], i["end"]] for i in taskDurations}

    for task in tasks:
        "2022-11-12T23:00:00.000Z"
        start, end = taskDurations[task]
        start = datetime.datetime(
            year=int(start.split("T")[0].split("-")[0]),
            month=int(start.split("T")[0].split("-")[1]),
            day=int(start.split("T")[0].split("-")[2]) + 1,
        )

        end = datetime.datetime(
            year=int(end.split("T")[0].split("-")[0]),
            month=int(end.split("T")[0].split("-")[1]),
            day=int(end.split("T")[0].split("-")[2]) + 1,
        )

        duration = (end - start).days

        taskid, _ = tasks[task]

        model_task = Task.objects.get(taskid=taskid)

        if model_task.duration != duration:
            model_task.estimated = False
            model_task.duration = duration
            model_task.start = start
            model_task.save()

    # Rerun ML Classification Algorithm and reestimating the task durations
    run_classification()

    return HttpResponse(status=200)
