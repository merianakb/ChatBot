#CreatedOn 6/7/2020
from wit import Wit

from Category1 import cat1
from Category2 import cat2
from Category3 import cat3
from IntentDetector import intentDetector

def get_maxConfidence_intent(response):
    max_confidence=0
    index_intent=0
    i=0
    for intent in response['intents']:
        if(intent['confidence']>max_confidence):
            max_confidence=intent['confidence']
            index_intent=i
        i=i+1
    return index_intent


access_token1="47NSN4OXBXZVXQEDBHR6YKCJMITQJJKH"

client=Wit(access_token=access_token1)

message_text="when is the meeting of candidate Candidate17 for position senior engineer"
message_text2="when the interview is set for Candidate3"
message_text3="where and when the meeting is set for candidate17"

message_text4="name of accepted candidate for post senior engineer"
message_text5="name of not accepted candidate for senior engineer"

message_text6="which candidate has posted for senior engineer"
message_text13="who are the candidates  for position senior engineer"

message_text8="who has executed the offer publication activity"
message_text9="which actor has executed offer publication for  position senior engineer"
#message_text12="which actor has sent the meeting for Candidate3"

message_text14="For which positions Candidate3 has sent his application"
message_text15="which applications were selected"
message_text16="who received an email about interview wrapup"

msg10="name of accepted candidate for post senior engineer"
msg11="name of not accepted candidate for senior engineer"
msg12="which candidates have posted for senior engineer"
msg13=" who applied for engineer position"
msg14="which actor has executed the offer publication activity"
msg15="who has executed offer publication for position senior engineer"
msg16="who sent the interview setting for Candidate3"
msg17="which actor has sent the interview schedule for Candidate3"
msg18="name of all candidate"
msg19="artifact affected by actor LN"
msg20="all actors affected Candidate3"




def chatbot_response(msg):
    try:
        resp=client.message(msg)
        print(resp)
        print()
        if(len(resp['intents'])==0 or get_maxConfidence_intent(resp)<0.5):
            print(get_maxConfidence_intent(resp))
            return intentDetector.activate(resp)
    except:
        return "Error"


re=chatbot_response(msg13)
for  record in re:
            print (str(record))




