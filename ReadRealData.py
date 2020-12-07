import xlrd

from py2neo import Graph
from datetime import datetime

activity_list=[]
actor_list=[]

def floatHourToTime(fh):
    h, r = divmod(fh, 1)
    m, r = divmod(r*60, 1)
    return (
        int(h),
        int(m),
        int(r*60),
    )

graph=Graph('bolt://localhost:7687',auth=("neo4j","MyGraphP@ss"))

# Give the location of the file
loc = ("C:/Users/user/Desktop/Courses/Master2/Stage/MyPapers/chatbot/testing_data_v1.xlsx")

# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

i=2
while i<sheet.nrows:
    activity_name=sheet.cell_value(i,7)
    activity_nature=sheet.cell_value(i,17)
    activity_id=str(i)

    actor_from=sheet.cell_value(i,1)
    actor_cc=sheet.cell_value(i,2).split(";")
    actor_to=sheet.cell_value(i,3).split(";")
    actor_executor=sheet.cell_value(i,18)
    actor_requestor=sheet.cell_value(i,20)
    actor_requested=sheet.cell_value(i,21)

    print("activityname: "+activity_name+" /activitynature: "+activity_nature+" /from: "+actor_from+" /to:  "+actor_to[0])
    if activity_name not in activity_list:
        activity_list.append(activity_name)


    #create activity node
    query="CREATE (n: Activity {activityName: '"+activity_name+"',activityNature: '"+activity_nature+"' ,ID: '"+activity_id+"'})"
    try:
        data=graph.run(query)
    except:
        print("activity not created "+activity_name+"i")

    #create actor with hasSent relation
    query2="MERGE (m: Actor {actorEmail: '"+actor_from+"'})"
    try:
        data=graph.run(query2)
    except:
        print("actor not created "+actor_from)
    query3="MATCH (n: Actor{actorEmail: '"+actor_from+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:HasSent]->(m)"
    try:
        data=graph.run(query3)
    except:
        print("Error on creation relation")
    if actor_from not in actor_list:
        actor_list.append(actor_from)

    #create actor with hasReceived relation
    for actor in actor_to:
        actor=actor.strip()
        query2="MERGE (m: Actor {actorEmail: '"+actor+"'})"
        try:
            data=graph.run(query2)
        except:
            print("actor not created "+actor)
        query3="MATCH (n: Actor{actorEmail: '"+actor+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:HasReceived]->(m)"
        try:
            data=graph.run(query3)
        except:
            print("Error on creation relation")
        if actor not in actor_list:
            actor_list.append(actor)

     #create actor with hasObserved relation
    for actor in actor_cc:
        actor=actor.strip()
        query2="MERGE (m: Actor {actorEmail: '"+actor+"'})"
        try:
            data=graph.run(query2)
        except:
            print("actor not created "+actor)
        query3="MATCH (n: Actor{actorEmail: '"+actor+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:HasObserved]->(m)"
        try:
            data=graph.run(query3)
        except:
            print("Error on creation relation")
        if actor not in actor_list:
            actor_list.append(actor)

    #create actor with hasExecuted relation
    query2="MERGE (m: Actor {actorEmail: '"+actor_executor+"'})"
    try:
        data=graph.run(query2)
    except:
        print("actor not created "+actor_executor)
    query3="MATCH (n: Actor{actorEmail: '"+actor_executor+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:HasExecuted]->(m)"
    try:
        data=graph.run(query3)
    except:
        print("Error on creation relation")
    if actor_executor not in actor_list:
            actor_list.append(actor_executor)

    #create actor with hasRequested relation
    query2="MERGE (m: Actor {actorEmail: '"+actor_requestor+"'})"
    try:
        data=graph.run(query2)
    except:
        print("actor not created "+actor_requestor)
    query3="MATCH (n: Actor{actorEmail: '"+actor_requestor+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:HasRequested]->(m)"
    try:
        data=graph.run(query3)
    except:
        print("Error on creation relation")
    if actor_requestor not in actor_list:
            actor_list.append(actor_requestor)

    #create actor with hasReceivedRequest relation
    query2="MERGE (m: Actor {actorEmail: '"+actor_requested+"'})"
    try:
        data=graph.run(query2)
    except:
        print("actor not created "+actor_requested)
    query3="MATCH (n: Actor{actorEmail: '"+actor_requested+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:HasReceivedRequest]->(m)"
    try:
        data=graph.run(query3)
    except:
        print("Error on creation relation")
    if actor_requested not in actor_list:
            actor_list.append(actor_requested)

    #Subject artifact
    subject=sheet.cell_value(i,8)
    if not len(subject)==0:
        query2="MERGE (m: Artifact {Type: 'Subject', subjectTitle: '"+subject+"'})"
        try:
            data=graph.run(query2)
        except:
            print("subject not created "+subject)
        query3="MATCH (m: Artifact {Type: 'Subject', subjectTitle: '"+subject+"'}),(n: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:AffectArtifact]->(m)"
        try:
            data=graph.run(query3)
        except:
            print("Error on creation relation")

    #Position artifact
    position=sheet.cell_value(i,10)
    if not len(position)==0:
        query2="MERGE (m: Artifact {Type:'Position', positionTitle: '"+position+"'})"
        try:
            data=graph.run(query2)
        except:
            print("position not created "+position)
        query3="MATCH (m: Artifact {Type:'Position', positionTitle: '"+position+"'}),(n: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:AffectArtifact]->(m)"
        try:
            data=graph.run(query3)
        except:
            print("Error on creation relation")

    #Interview artifact
    date=sheet.cell_value(i,11)
    time=str(sheet.cell_value(i,12))
    location=sheet.cell_value(i,13)
    if not len(str(date))==0:
        dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(date) - 2)
        hour, minute, second = floatHourToTime(date % 1)
        dt = dt.replace(hour=hour, minute=minute, second=second)
        dateString=dt.strftime("%d-%b-%Y")
        query2="MERGE (m: Artifact {Type:'Interview', interviewDate: '"+dateString+"', interviewTime: '"+time+"', interviewLocation: '"+location+"'})"
        try:
            data=graph.run(query2)
        except:
            print("interview not created ")
        query3="MATCH (m: Artifact {Type:'Interview', interviewDate: '"+dateString+"', interviewTime: '"+time+"', interviewLocation: '"+location+"'}),(n: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:AffectArtifact]->(m)"
        try:
            data=graph.run(query3)
        except:
            print("Error on creation relation")
        '''''
        #relation between interview and position
        position=sheet.cell_value(i,10)
        if not len(position)==0:
            query4="MATCH (m: Artifact {Type:'Interview', interviewDate: '"+dateString+"', interviewTime: '"+time+"', interviewLocation: '"+location+"'}),(n: Artifact {Type:'Position',  positionTitle:'"+position+"'})" \
                "MERGE (m)-[:Concerning]->(n)"
            try:
                data=graph.run(query4)
            except:
                print("Error on creation relation")
        '''

     #Candidate artifact
    candidate=sheet.cell_value(i,16).split(",")
    if not len(candidate)==0:
        for cand in candidate:
            cand=cand.strip()
            query2="MERGE (m: Artifact {Type:'Candidate', candidateName: '"+cand+"'})"
            try:
                data=graph.run(query2)
            except:
                print("candidate not created "+cand)
            query3="MATCH (m: Artifact {Type:'Candidate', candidateName: '"+cand+"'}),(n: Activity { ID:'"+activity_id+"'})" \
                    "MERGE (n)-[:AffectArtifact]->(m)"
            try:
                data=graph.run(query3)
            except:
                print("Error on creation relation")
            '''''
            #relation between interview and candidate
            date=sheet.cell_value(i,11)
            if not len(str(date))==0:
                query4="MATCH (m: Artifact {Type:'Interview', interviewDate: '"+dateString+"', interviewTime: '"+time+"', interviewLocation: '"+location+"'}),(n: Artifact { Type:'Candidate', candidateName: '"+cand+"'})" \
                "MERGE (m)-[:ForCandidate]->(n)"
                try:
                    data=graph.run(query4)
                except:
                    print("Error on creation relation")
             #relation between position and candidate
            position=sheet.cell_value(i,10)
            if not len(position)==0:
                query4="MATCH (m: Artifact {Type:'Position', positionTitle: '"+position+"'}),(n: Artifact {Type:'Candidate',  candidateName: '"+cand+"'})" \
                    "MERGE (n)-[:AppliedFor]->(m)"
                try:
                    data=graph.run(query4)
                except:
                    print("Error on creation relation")
            '''


    #Application artifact
    number=sheet.cell_value(i,14).split(",")
    status=sheet.cell_value(i,15)
    if not len(number)==0:
        for num in number:
            num=num.strip()
            query2="MERGE (m: Artifact {Type:'Application', applicationNumber: '"+num+"'})"
            try:
                data=graph.run(query2)
            except:
                print("application not created "+num)
            query3="MATCH (m: Artifact {Type:'Application', applicationNumber: '"+num+"'}),(n: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:AffectArtifact]->(m)"
            try:
                data=graph.run(query3)
            except:
                print("Error on creation relation")

            if not len(status)==0: #accepted or rejected
                candidate=sheet.cell_value(i,16).split(",")
                for cand in candidate:
                    cand=cand.strip()
                    query3="MATCH (m: Artifact {Type:'Candidate', candidateName: '"+cand+"'}),(n: Artifact {Type:'Position', positionTitle:'"+position+"'})" \
                            "MERGE (m)-[:"+status+"]->(n)"
                    try:
                        data=graph.run(query3)
                    except:
                        print("Error on creation relation")
                    query3="MATCH (m: Artifact {Type:'Application', applicationNumber: '"+num+"'}),(n: Artifact {Type:'Position', positionTitle:'"+position+"'})" \
                        "MERGE (m)-[:"+status+"]->(n)"
                    try:
                        data=graph.run(query3)
                    except:
                        print("Error on creation relation")
            '''''
            #relation between application and position
            position=sheet.cell_value(i,10)
            if not len(position)==0:
                    query4="MATCH (m: Artifact {Type:'Position', positionTitle: '"+position+"'}),(n: Artifact { Type:'Application', applicationNumber: '"+num+"'})" \
                        "MERGE (n)-[:Concerning]->(m)"
                    try:
                        data=graph.run(query4)
                    except:
                        print("Error on creation relation")

            #relation between application and candidate
            candidate=sheet.cell_value(i,16).split(",")
            if not len(candidate)==0:
                for cand in candidate:
                    cand=cand.strip()
                    query4="MATCH (m: Artifact {Type:'Candidate', candidateName: '"+cand+"'}),(n: Artifact {Type:'Application',  applicationNumber: '"+num+"'})" \
                        "MERGE (n)-[:ForCandidate]->(m)"
                    try:
                        data=graph.run(query4)
                    except:
                        print("Error on creation relation")
            '''



    i=i+1
