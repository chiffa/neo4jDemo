'''
Created on 20 August 2013

@author: Andrei
'''

from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, Float, Dictionary, List

class CostumNode(Node):             # Serves as a basis for the annotation
    element_type="CostumNode"
    ID=String(nullable=False)       # Fixed IDs to allow interoperability between different DB versions
    displayName=String()            # To see what it is, for the human operator
    custom=String()                 # Just in case
    
class AnnotNode(Node):
    element_type="AnnotNode"        # To store personal annotations
    Type=String()                   # Attention, jobtype, etc...
    Content=String(nullable=False)  # contains the information load for the annotation
    
class Person(CostumNode):
    element_type="Person"
    name=String(nullable=False)
    birthdate=String()
    birhtplace=String()
    
class Handle(AnnotNode):            # e-mail address, name, pseudo // If fulltext search doesn't work, add name and 
    element_type="Handle"

class Organisation(CostumNode):
    element_type="Organisation"
    type=String()
    Name=String(nullable=False)

class MailingList(CostumNode):
    element_type="MailingList"
    
class belongs_to(Relationship):
    label="belongs_to"
    role=String()
    
class describes(Relationship):
    label="describes"





