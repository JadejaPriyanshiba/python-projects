import re
from generals import array
# validate topics given, modify list accordingly
class ValidateTopics:
    topicsByAI = []

    instructions = """ ~~~~ INSTRUCTIONS ~~~~

~ Enter 'ok' if the list seems perfect,
~ Enter 'instruct' to get instructions again,
~ Enter 'recap' for instruction summary, 
~ Enter 'list' for printing list again, 

~ to add a topic at last enter 'a:' and new topic name, like 'a: this is the new topic',
~ to add a topic at specific index enter 'a' with index and new topic name, like 'a3: this is the new topic',
~ to add many topics at any or last you can combine things like: '[a: this is new last topic],[a3: this topic will be added at index 3],[a: this topic will be last]'

~ to modify the sequence of the list enter old_index + '->' + new_index, like '2->3'
    NOTE: be very specific about the syntax,
          this will move up/down the remaining topics accordingly, like will move other topics up if topic moved down, or vive-versa
~ to modify index (interchange the indexes), enter old_index + '<->' + new_index, like '2<->3'

~ to modify a topic, enter 'm' with index and modified topic, like 'm1: new topics title', make sure you don't use ':', you can use '()' instead,
~ to modify many topics you can enter like '[m1: new title for index 1],[m4: new title for index 4],[m6: new title for index 6]'

~ to remove any topic, enter 'r' with index like 'r1' to remove first topic
~ to remove many topics enter topics index with 'r' like 'r1,r4,r7'
    """

    instruction_recap=""" ~~~~ INSTRUCTIONS RECAP ~~~~
~ 'ok'
~ 'instruct'
~ 'recap'
~ 'list'
~ ADD:
    1. a: new topic at last
    2. a2: new topic at a index
    3. [a: new topic at last],[a2: new topic at a index],[a: new topic at last]
~ REMOVE:
    1. r1
    2. r2,r5,r6
~ MODIFY:
    1. m1: modified topic at index 1
    2. [m3: modified topic at index 3],[m5: modified topic at index 5],[m8: modified topic at index 8]
~ SEQUENCE:
    1. 2->4
    2. 2<->4 
    """

    def __init__(self, topics):
        self.topicsByAI = topics

    def validateTopics(self):
        if( type(self.topicsByAI) is not list or self.topicsByAI==[]):
            raise Exception("invalid input")
        
        self.__printList()
        print(self.instructions)
        self.__getAndProcessInput()
    
    def __getAndProcessInput(self):
        flag = True
        text = "No Change made"
        while flag:
            key = input("Enter your input: ").strip()

            # if the list is perfect
            if(key == "ok"):
                flag = False
                text = "generating notes"
            # if user wants instructions again
            elif(key == "instruct"):
                print(self.instructions)
                text = ""
            # if wants instruction recap
            elif(key == 'recap'):
                print(self.instruction_recap)
                text = ""
            #printing list again
            elif(key == "list"):
                self.__printList()
            # if addition
            elif(key[0]=='a'):
                self.__manageAdd(key)
                text = "Added topic to list"
            # if multiple addition
            elif(re.fullmatch(r'^\[(a\d+: [^\]]+)\](,\[(a\d+: [^\]]+)\])*$', key)):
                self.__manageMultipleAdd(key)
                text = "Added topics to list"
            # if removal
            elif(key[0]=='r'):
                self.__manageRemove(key)
                text = "Removed topic from list"
            # if sequence change
            elif(key[0].isnumeric and re.match(r"^\d+(->|<->)\d+$", key)):
                self.__manageSequence(key)
                text = "Changed sequence of the list"
            # modify topics 
            elif(key[0]=='m'):
                self.__manageModify(key)
                text = "Modified topic of the list"
            # manage multiple modify
            elif(re.fullmatch(r'^\[(m\d+: [^\]]+)\](,\[(m\d+: [^\]]+)\])*$', key)):
                self.__manageMultipleModify(key)
                text = "Modified topics of the list"
            # if none of it matches
            else:
                print("Invalid input")

            # reprinting list for verfication
            if(text!=""):
                self.__printList(text=text)

    def __manageAdd(self, key):
        key = str(key)
        
        # add at first
        if(key[0:2]=="a:"):
            topic = key[2:]
            self.topicsByAI.append(topic.strip())
        # add at index
        elif (key[1].isnumeric):
            index = int(key[1])-1
            topic = key[3:].strip()
            self.topicsByAI.insert(index, topic)
        else:
            print("Invalid format, something went wrong, your key: ",key)

    # manage multiple adds
    def __manageMultipleAdd(self, key):
        key = str(key)
        topicsToAdd = key.split(key,"],[")

        # handle each topic
        for i in topicsToAdd:
            i = i.replace("[","").replace("]","").strip()
            self.__manageAdd(i)
    
    # manage single modify
    def __manageModify(self,key):
        key = str(key)
        
        if (key[0]=="m" and key[1].isnumeric):
            index = int(key[1])-1
            topic = key[3:].strip()
            self.topicsByAI[index] = topic
        else:
            print("Invalid format, something went wrong, your key: ",key)
    
    # manage multiple modifications
    def __manageMultipleModify(self, key):
        key = str(key)
        topicsToAdd = key.split(key,"],[")

        # handle each topic
        for i in topicsToAdd:
            i = i.replace("[","").replace("]","").strip()
            self.__manageModify(i)

    # manage removals
    def __manageRemove(self, key):
        key = str(key)
        indexes = key.split(",")
        tempList = self.topicsByAI
        # loping and removing
        for i in indexes:
            if(i[0]=="r" and i[1].isnumeric()):
                index = int(i[1])-1
                tempList.remove(self.topicsByAI[index])
            else:
                print(f"invalid format in {key}, {i}")
        self.topicsByAI = tempList
    
    # manage sequence
    def __manageSequence(self, key):
        key = str(key).strip()

        if(key[0].isnumeric() and key[-1].isnumeric()):
            index1 = key[0]
            index2 = key[-1]
                
            # if interchange
            if(len(key)==4 and key.find("<->")!= -1):
                value1 = key[index1]
                key[index1] = key[index2]
                key[index2] = value1
            # interchange the values
            elif(len(key)==3 and key.find("->")!=-1):
                self.topicsByAI = array.moveElement(self.topicsByAI, index1, index2)
        else:
            print("Invalid format, you key was: ", key)
        
    # print topic list
    def __printList(self, text= "These topics covered will be: "):

        print(text)
        for i in self.topicsByAI:
            print(f"{self.topicsByAI.index(i)+1}) {i}")
        
