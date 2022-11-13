from .models import *
import pandas as pd
import os

def parse_to_model(path, project_id):
    # Load csv file into panda data frame
    df = pd.read_csv(path)

    # Get all different groups in csv file
    group, groups = list(), list()
    for row in df.index:
        row = df.loc[[row]]
        group.append(row)
        if row["i"].sum() == 0:
            groups.append(group)
            group = []

    p = Project.objects.create(id=project_id)

    # Save individual Tasks of each group
    for group in groups:
        for item in group:
            print(item)
            Task.objects.create(
                taskid=list(item["id"])[0],
                project_id=p.id,
                quantity=list(item["quantity"])[0],
                qu=list(item["qu"])[0],
                outline_text=list(item["outline_text"])[0],
                detail_text=list(item["detail_text"])[0],
            )



def get_csv():
    directory = "/Users/timruppert/Downloads/SDaCathon2022 - Terminplanung/out"
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        filepath = os.path.join(directory, filename)
        parse_to_model(filepath, filename)





