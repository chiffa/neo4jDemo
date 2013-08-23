'''
Created on Aug 21, 2013

@author: andrei
'''

from neo4j_connector import DatabaseGraph
import string
import random
from time import time

Persons=["Philip Bourne", "Peter Rose", "Spencer Blieven", "Andreas Prlic", "Li Xie", "Ann Kagheiro", "Andrei Kucharavy", "Julia Ponomarenko", "Cole Christie"]
#        0                1                2                3                4                5                6                7                8
Organizations=["RSCB PDB", "PLoS Bioinformatics", "Bourne Lab", "Innovation and Industrial Alliances at UCSD", "BioJava", "UCSD", "EPFL","Ecole Polytechnique", "SDSC"]
#                0            1                    2                3                                            4            5    6        7                    8
Mails=["c@ucsd.edu","b@sdsc.edu","a@sdsc.edu","sn@ucsd.edu","p@ucsd.edu","l@ucsd.edu","k@sdsc.edu", "j@sdsc.edu", "a@ucsd.edu","a.k@epfl.ch"]
#        0                    1                    2                3                    4                5                6                    7                8                        9
HandlesPlus=["Phil","Pete","andrei_chiffa","chiffa"]
#            0        1        2            3

O2O={0:5,2:5,3:5,8:5}
P2O={0:[(0,"Associate director"),(1,"co-founding editor"),(2,"director"),(3,"vice-chancelor"),(8,"")],
     1:[(0,"Leading Scientist")],
     2:[(2,"PhD student")],
     3:[(0,"SeniorScientist"),(4,"ProjectLeader"),(1,"Software Editor"),(8,"")],
     4:[(2,"Post-Doc")],
     5:[(2,""),(8,"")],
     6:[(6,"Master student"),(2,"visiting grad"),(7,"engineering student")],
     7:[(8,"PI")],
     8:[(0,"")],
     }

P2Mail={0:[1],
        1:[4],
        2:[3],
        3:[2],
        4:[5],
        5:[6],
        6:[8,9],
        7:[7],
        8:[0],
        }

P2OH={0:[0],
      1:[1],
      6:[2,3],
      }

Anns_maillist=[0,1,2,3,4,5,6,7,]


def generateRandomData(PersonNum=10000,OrganisationNum=5000,MailDens=2,MailStd=0.5,OrgDens=3,OrgStd=2,O2ODens=2,O2OStdev=2):

    domains=['.edu','.org','.com','.net']
    providers=[]
    for i in range(0,OrganisationNum*2):
        Name=''.join(random.choice(string.ascii_lowercase) for x in range(10))
        providers.append(Name)
    
    for i in range(0,OrganisationNum):
        Name=''.join(random.choice(string.ascii_lowercase) for x in range(20))
        Organizations.append(Name)

    for i in range(0,PersonNum):
        Name=''.join(random.choice(string.ascii_lowercase) for x in range(15))
        Surname=''.join(random.choice(string.ascii_lowercase) for x in range(15))
        FullName=Name+' '+Surname
        Persons.append(FullName)
        
        OrgNums=int(round(abs(random.gauss(OrgDens,OrgStd))))
        OrgIndexes=range(0,OrganisationNum)
        random.shuffle(OrgIndexes)
        tmpList=[]
        for elt in OrgIndexes[:OrgNums]:
            tmpList.append((elt,""))
        if i not in P2O.keys():
            P2O[i]=tmpList
        
        MailNum=int(round(abs(random.gauss(MailDens,MailStd))))
        tmpList2=[]
        for i in range(0,MailNum):
            Name=''.join(random.choice(string.ascii_lowercase) for x in range(15))
            random.shuffle(providers)
            random.shuffle(domains)
            Name=Name+providers[0]+domains[0]
            tmpList2.append(len(Mails))
            Mails.append(Name)
            
        if i not in P2O.keys():
            P2Mail[i]=tmpList2

def create():
    Pers_Dict={}
    Org_Dict={}
    Mail_Dict={}
    Handle_Dict={}
    counter=0
    i=0
    init=time()
    counter_prev=0
    for person in Persons:
        counter+=3
        if counter%100==99:
            print counter,'\t', "{0:.2f}".format(time()-init), '\t',  "{0:.2f}".format((counter-counter_prev)/(time()-init)), 'insertions/sec'
            init=time()
            counter_prev=counter
        Node=DatabaseGraph.Person.create(ID=str(counter),name=person,displayName=person)
        Pers_Dict[i]=Node
        Node2=DatabaseGraph.Handle.create(Type="name",Content=person)
        DatabaseGraph.describes.create(Node,Node2)
        i+=1
    i=0
    for org in Organizations:
        counter+=1
        if counter%100==99:
            print counter,'\t', "{0:.2f}".format(time()-init), '\t',  "{0:.2f}".format((counter-counter_prev)/(time()-init)), 'insertions/sec'
            init=time()
            counter_prev=counter
        Node=DatabaseGraph.Organisation.create(ID=str(counter),Name=org,displayName=org)
        Org_Dict[i]=Node
        i+=1
    i=0
    for mail in Mails:
        counter+=1
        if counter%100==99:
            print counter,'\t', "{0:.2f}".format(time()-init), '\t',  "{0:.2f}".format((counter-counter_prev)/(time()-init)), 'insertions/sec'
            init=time()
            counter_prev=counter
        Node=DatabaseGraph.Handle.create(ID=str(counter),Type="e-mail adress",Content=mail)
        Mail_Dict[i]=Node
        i+=1
    i=0
    for handle in HandlesPlus:
        counter+=1
        if counter%100==99:
            print counter,'\t', "{0:.2f}".format(time()-init), '\t',  "{0:.2f}".format((counter-counter_prev)/(time()-init)), 'insertions/sec'
            init=time()
            counter_prev=counter
        Node=DatabaseGraph.Handle.create(ID=str(counter),Type="alias",Content=handle)
        Handle_Dict[i]=Node
        i+=1
    MailList=DatabaseGraph.MailingList.create(ID=str(counter+1),displayName="Ann's Mail List")
    print '======================================================================/n Strarting relations /n ======================================================================'
    
    for link in O2O.iteritems():
        counter+=1
        if counter%100==99:
            print counter,'\t', "{0:.2f}".format(time()-init), '\t',  "{0:.2f}".format((counter-counter_prev)/(time()-init)), 'insertions/sec'
            init=time()
            counter_prev=counter
        DatabaseGraph.belongs_to.create(Org_Dict[link[0]],Org_Dict[link[1]])
    for sup_link in P2O.iteritems():
        for sub_link in sup_link[1]:
            counter+=1
            if counter%100==99:
                print counter,'\t', "{0:.2f}".format(time()-init), '\t',  "{0:.2f}".format((counter-counter_prev)/(time()-init)), 'insertions/sec'
                init=time()
                counter_prev=counter
            link=(sup_link[0],sub_link)
            DatabaseGraph.belongs_to.create(Pers_Dict[link[0]],Org_Dict[link[1][0]],role=link[1][1])
    for sup_link in P2Mail.iteritems():
        for sub_link in sup_link[1]:
            counter+=1
            if counter%100==99:
                print counter,'\t', "{0:.2f}".format(time()-init), '\t',  "{0:.2f}".format((counter-counter_prev)/(time()-init)), 'insertions/sec'
                init=time()
                counter_prev=counter
            link=(sup_link[0],sub_link)
            DatabaseGraph.describes.create(Pers_Dict[link[0]],Mail_Dict[link[1]])
    for sup_link in P2OH.iteritems():
        for sub_link in sup_link[1]:
            link=(sup_link[0],sub_link)
            counter+=1
            if counter%100==99:
                print counter,'\t', "{0:.2f}".format(time()-init), '\t',  "{0:.2f}".format((counter-counter_prev)/(time()-init)), 'insertions/sec'
                init=time()
                counter_prev=counter
            DatabaseGraph.describes.create(Pers_Dict[link[0]],Handle_Dict[link[1]])
    for mail in Anns_maillist:
        DatabaseGraph.belongs_to.create(MailList,Mail_Dict[mail],role="")
    DatabaseGraph.belongs_to.create(MailList,Pers_Dict[5],role="owner")
        
def clear():
    for node in DatabaseGraph.vertices.get_all():
        ID=str(node).split('/')[-1][:-1]
        DatabaseGraph.vertices.delete(ID)

def show():
    for node in DatabaseGraph.Person.get_all():
        ID=str(node).split('/')[-1][:-1]
        DispName=node.displayName
        print ID, DispName

    for node in DatabaseGraph.Organisation.get_all():
        ID=str(node).split('/')[-1][:-1]
        DispName=node.displayName
        print ID, DispName

# generateRandomData()
# clear()
create()
show()

def get_mail(PartialName):
    quer="Content:"+PartialName 
    vertices = DatabaseGraph.Handle.index.query(quer)
    if vertices==None:
        return "No such handle!"
    buffer=""
    mails=[]
    for vertex in vertices:
        buffer+=vertex.Type+' '+vertex.Content+'\n'
        gen=vertex.inV("describes")
        if gen!=None:
#         if True:
            for person in gen:
                buffer+='\t'+person.displayName+'\t@'
                for organisation in person.outV("belongs_to"):
                    buffer+=' '+organisation.displayName+' |'
                buffer+='\n'
                gen2=person.outV("describes")
                for handle in gen2:
                    if handle.Type=="e-mail adress":
                        buffer+='\t\t'+handle.Content+'\n'
                        mails.append(handle)
#     print buffer
    return buffer, mails

def getLists(UserName):
    quer="Content:"+UserName 
    vertices = DatabaseGraph.Handle.index.query(quer)
    if vertices==None:
        return "No such handle!"
    buffer=""
    mailLists=[]
    for vertex in vertices:
        buffer+=vertex.Type+' '+vertex.Content+'\n'
        gen=vertex.inV("describes")
        if gen!=None:
#         if True:
            for person in gen:
                buffer+='\t'+person.displayName+'\t@'
                for organisation in person.outV("belongs_to"):
                    buffer+=' '+organisation.displayName+' |'
                buffer+='\n'
                gen2=person.inV("belongs_to")
                for mailList in gen2:
                    if mailList.element_type=="MailingList":
                        buffer+='\t\t'+mailList.displayName+'\n'
                        mailLists.append(mailList)
#     print buffer
    return buffer, mailLists

def addToList(MailLists,mails):
    for MailList in MailLists:
        for mail in mails:
            DatabaseGraph.belongs_to.create(MailList,mail,role="")

init=time()
for i in range(0,99):
    get_mail('Andrei')  
    get_mail('Bourne')
    get_mail('Phil')
print get_mail('Andrei')  
print get_mail('Bourne')
print get_mail('Phil')
print (time()-init)/100


