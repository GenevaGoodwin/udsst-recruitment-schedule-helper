from drafter import *
from dataclasses import dataclass

@dataclass
class Course:
    start: str
    end: str
    
@dataclass
class Activity:
    start: str
    end: str
    
@dataclass
class TeamMember:
    name: str
    courses: list[Course]
    
@dataclass
class State:
    team: list[TeamMember]
    main_schedule: list[Activity]

@route
def add_member (state: State) -> Page:
    return Page(state, [TextBox("Enter Full Name:", TeamMember.name),
                        Button("Add Class", "add_course"),
                        Button ("Return to Homepage", "index")])
    
@route
def 







@route
def index (state: State) -> Page:
    return Page(state, [Button("Add Team Member", "add_member"),
                        Button("Add Main Schedule", "add_to_main_schedule"),
                        Button("View Group Availability", "group_availability")])
        

