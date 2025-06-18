import re

# validate topics given, modify list accordingly
class validateTopics:
    topicsByAI = []

    instructions = """ ~~~~ INSTRUCTIONS ~~~~

~ Enter 'ok' if the list seems perfect,
~ Enter 'instruct' to get instructions again,
~ Enter 'recap' for instruction summary, 

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
    
    def __getAndProcessInput(self):
        flag = True
        while flag:
            key = input("Enter your input: ").strip().lower()

            # if the list is perfect
            if(key == "ok"):
                flag = False
            
            # if user wants instructions again
            elif(key == "instruct"):
                print(self.instructions)
            
            # if wants instruction recap
            elif(key == 'recap'):
                print(self.instruction_recap)

            # if addition
            elif(key[0]=='a'):
                self.__manageAdd(key)
            
            # if removal
            elif(key[0]=='r'):
                self.__manageRemove(key)
            
            # if sequence change
            elif(key[0].isnumeric and re.match(r"^\d+(->|<->)\d+$", key)):
                self.__manageSequence(key)
            
            # modify topics 
            elif(key[0]=='m'):
                pass
            
            # if none of it matches
            else:
                print("Invalid input")

    def __manageAdd(self, key):
        pass
    def __manageModify(self,key):
        pass
    def __manageRemove(self, key):
        pass
    def __manageMultiple(self, key):
        pass
    def __manageSequence(self, key):
        pass



        
    
    def __printList(self, text= "These topics covered will be: "):

        print(text)
        for i in self.topicsByAI:
            print(f"{self.topicsByAI.index(i)+1}) {i}")
        
