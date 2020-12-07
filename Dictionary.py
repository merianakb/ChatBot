from collections import defaultdict

nodes=["Actor","Activity","Artifact"]
artifactNodes=["Position","Candidate","Interview","Application","Subject"]
edge= {"Actor":["Actvity"],
       "Activity":["Actor","Position","Candidate","Interview","Application","Activity","Subject"],
       "Candidate":["Position","Activity"],
       "Interview":["Activity"],
       "Application":["Position","Activity"],
       "Position":["Application","Candidate","Activity"]}

relationName = defaultdict(dict)

relationName['Actor']['Activity']=['HasExecuted','HasSent','HasReceived','HasObserved','HasRequested','HasReceivedRequest']
relationName['Activity']['Actor']=['HasExecuted','HasSent','HasReceived','HasObserved','HasRequested','HasReceivedRequest']

relationName['Activity']['Activity']=['FollowedBy','PFollowedBy','AFollowedBy','IFollowedBy','CFollowedBy']

relationName['Activity']['Artifact']=['AffectArtifact']
relationName['Artifact']['Activity']=['AffectArtifact']

relationName['Activity']['Position']=['AffectArtifact']
relationName['Position']['Activity']=['AffectArtifact']

relationName['Activity']['Candidate']=['AffectArtifact']
relationName['Candidate']['Activity']=['AffectArtifact']

relationName['Activity']['Interview']=['AffectArtifact']
relationName['Interview']['Activity']=['AffectArtifact']

relationName['Activity']['Application']=['AffectArtifact']
relationName['Application']['Activity']=['AffectArtifact']

relationName['Activity']['Subject']=['AffectArtifact']
relationName['Subject']['Activity']=['AffectArtifact']

relationName['Candidate']['Position']=['accepted','rejected']
relationName['Position']['Candidate']=['accepted','rejected']


relationName['Application']['Position']=['accepted','rejected']
relationName['Position']['Application']=['accepted','rejected']




def getRelationBetweenTwoNodes(node1,node2):
    return relationName[node1][node2]

def getNodesHavingRelationWith(node):
    for item in edge:
        if item==node:
            return edge[item]
    return []

def getDestinationNode(node,relation):
    keyA=node
    for keyB in relationName[keyA]:
        if(relation in relationName[keyA][keyB]):
            return keyB
    return ""

def ifRelationExist(node1,node2):
    keyA=node1
    keyB=node2
    if (keyA in relationName) & (keyB in relationName[keyA]):
        return 1
    return 0

def RelationExist(node1,node2,relation):
     keyA=node1
     keyB=node2
     relations=relationName[keyA][keyB]
     if(relation in relations):
         return 1
     return 0

def getNodesOfRelation(relation):
    for keyA in relationName:
        for keyB in relationName[keyA]:
            if(relation in relationName[keyA][keyB] ):
                return keyA,keyB
    return "",""

def isArtifactNode(s):
    if(s=='position' or s=='candidate' or s=='application' or s=='interview' or s=='application'):
        return 1
    return 0
def isRoleNode(s):
    if(s=='role'):
        return 1
    return 0
def isActorNode(s):
    if(s=='actor'):
        return 1
    return 0
def isActivityNode(s):
    if(s=='activity'):
        return 1
    return 0







