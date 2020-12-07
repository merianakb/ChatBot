import Category1
import Category2
import Category3
import Dictionary
import NodeRelationDetector
from NodeRelationDetector import nodeRelationDetector
from StringExtractor import stringExtractor

from Category1 import  cat1
'''''
entityNodes=[]
entityAttributes={}
entityRelation=[]
returned_attributes=[]
nodeNb=0
relationNb=0
roleNodeNb=0
actorNodeNb=0
activityNodeNb=0
artifactNodeNb=0
constraints_attribute=[]
constraints_value=[]
'''

def get_maxConfidence_entities(response,entity):
        max_confidence=0
        index_entity=0
        i=0
        for ent in response['entities'][entity]:
            if(ent['confidence']>max_confidence):
                max_confidence=ent['confidence']
                index_entity=i
            i=i+1
        return index_entity

def get_returned_attributes(response,node):
    for item in response['entities']:
        str_item=str(item) #positionType:positionType
        str_item=str_item.split(':')[0]
        if(str_item.endswith("KeyWord") and str_item.startswith(node)):
            att=stringExtractor.getReturnedAttributeName(str_item)
            returned_attributes.append(att)
    return returned_attributes

def findCategory():
    print(entityNodes)
    print(entityAttributes)
    print(entityRelation)

    #category 1
    if(nodeNb==1 ):
        for item in entityAttributes:
            constraints_attribute.append(item)
            constraints_value.append(entityAttributes[item])
        if(relationNb==0):
            return Category1.execute_query(entityNodes[0].title(),returned_attributes,constraints_attribute,constraints_value)

    #category 3 (3 artifact nodes)
    elif(nodeNb==3 and artifactNodeNb==3):

        constraints_attribute1= []
        constraints_value1= []

        constraints_attribute2= []
        constraints_value2= []
        for item in entityAttributes:
            if(item.startswith(entityNodes[1])): #start with position or candidate...
                constraints_attribute1.append(item) #positionType
                constraints_value1.append(entityAttributes[item])
            elif(item.startswith(entityNodes[2])):#entityNode[0] is the returned node
                constraints_attribute2.append(item)
                constraints_value2.append(entityAttributes[item])
        return Category3.execute_query(entityNodes[0].title(),entityNodes[1].title(),entityNodes[2].title(),returned_attributes,constraints_attribute1,constraints_value1,
                  constraints_attribute2,constraints_value2)


    return nodeRelationDetector.activate(entityNodes,entityRelation,entityAttributes,returned_attributes)

class intentDetector(object):
    def activate(resp):
        global entityNodes
        global entityAttributes
        global entityRelation
        global returned_attributes
        global nodeNb
        global relationNb
        global roleNodeNb
        global actorNodeNb
        global activityNodeNb
        global artifactNodeNb
        global constraints_attribute
        global constraints_value
        entityNodes=[]
        entityAttributes={}
        entityRelation=[]
        returned_attributes=[]
        nodeNb=0
        relationNb=0
        roleNodeNb=0
        actorNodeNb=0
        activityNodeNb=0
        artifactNodeNb=0
        constraints_attribute=[]
        constraints_value=[]
        for item in resp['entities']:
            str_item=str(item)
            str_item=str_item.split(":")[0]
            if(str_item.endswith("Node")):

                if(str_item.endswith("ArtifactNode")):
                    #get name of artifact node
                    nodeName=stringExtractor.getName(str_item)
                    if(not nodeName  in entityNodes):
                        entityNodes.insert(0,nodeName)
                        nodeNb=nodeNb+1
                        artifactNodeNb=artifactNodeNb+1
                if(str_item.endswith('activityNode')):
                    if(not 'activity'  in entityNodes):
                        entityNodes.insert(0,'activity')
                        nodeNb=nodeNb+1
                        activityNodeNb=activityNodeNb+1
                if(str_item.endswith('actorNode')):
                    if(not 'actor' in entityNodes):
                        entityNodes.insert(0,'actor')
                        nodeNb=nodeNb+1
                        actorNodeNb=actorNodeNb+1
                if(str_item.endswith('roleNode')):
                    if(not 'role'  in entityNodes):
                        entityNodes.insert(0,'role')
                        nodeNb=nodeNb+1
                        roleNodeNb=roleNodeNb+1
                if(str_item.endswith('artifactNode')):
                    if(not 'artifact'  in entityNodes):
                        entityNodes.insert(0,'artifact')
                        nodeNb=nodeNb+1

            elif(str_item.endswith('Relation')):
                relationName=stringExtractor.getRelationName(str_item)
                entityRelation.insert(0,relationName)
                relationNb=relationNb+1
            elif(str_item.endswith("KeyWord")):
                attribute=stringExtractor.getReturnedAttributeName(str_item)
                nodeExtracted=stringExtractor.getName(attribute)
                if not nodeExtracted in entityNodes:
                    entityNodes.insert(0,nodeExtracted)
                    nodeNb=nodeNb+1
                    if(Dictionary.isArtifactNode(nodeExtracted)==1):
                        artifactNodeNb=artifactNodeNb+1
                    if(Dictionary.isActivityNode(nodeExtracted)==1):
                        activityNodeNb=activityNodeNb+1
                    if(Dictionary.isActorNode(nodeExtracted)==1):
                        actorNodeNb=actorNodeNb+1
                    if(Dictionary.isRoleNode(nodeExtracted)==1):
                        roleNodeNb=roleNodeNb+1
            elif(not str_item.endswith("KeyWord") and not str_item.endswith("Node") and not str_item.endswith("Relation")):
                attributeNode=stringExtractor.getName(str_item)
                index_item=get_maxConfidence_entities(resp,str_item+":"+str_item)
                if not attributeNode in entityNodes:
                    entityNodes.insert(0,attributeNode)
                    nodeNb=nodeNb+1
                    if(Dictionary.isArtifactNode(attributeNode)==1):
                        artifactNodeNb=artifactNodeNb+1
                    if(Dictionary.isActivityNode(attributeNode)==1):
                        activityNodeNb=activityNodeNb+1
                    if(Dictionary.isActorNode(attributeNode)==1):
                        actorNodeNb=actorNodeNb+1
                    if(Dictionary.isRoleNode(attributeNode)==1):
                        roleNodeNb=roleNodeNb+1
                entityAttributes[str_item.split(":")[0]]=resp['entities'][item][index_item]['value']

        returned_attributes=get_returned_attributes(resp,entityNodes[0])
        return findCategory()

def emptyAllArray():
    global entityNodes
    global entityAttributes
    global entityRelation
    global returned_attributes
    global nodeNb
    global relationNb
    global roleNodeNb
    global actorNodeNb
    global activityNodeNb
    global artifactNodeNb
    global constraints_attribute
    global constraints_value
    entityNodes=[]
    entityAttributes={}
    entityRelation=[]
    returned_attributes=[]
    nodeNb=0
    relationNb=0
    roleNodeNb=0
    actorNodeNb=0
    activityNodeNb=0
    artifactNodeNb=0
    constraints_attribute=[]
    constraints_value=[]





