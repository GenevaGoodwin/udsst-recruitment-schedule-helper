from drafter import *
from dataclasses import dataclass

@dataclass
class Time:
    start: str
    end: str
@dataclass
class Course:
    name: str
    time: Time
    
@dataclass
class Activity:
    name: str
    time: Time
@dataclass
class TeamMember:
    name: str
    courses: list[Course]
    
@dataclass
class State:
    team: list[TeamMember]
    main_schedule: list[Activity]
    active_member: str

@route
def add_member (state: State) -> Page:
    return Page(state, ["Enter Full Name:", TextBox("member_name"),
                        Button("Add Class", "submit_member"),
                        Button ("Return to Homepage", "index")])
    
@route
def submit_member (state: State, member_name) -> Page:
    state.active_member = member_name
    return Page(add_course)

@route
def add_course (state: State) -> Page:
    return Page(state, ["Class Name:", TextBox("class_name"),
                        "Class Start Time:", TextBox("class_start"),
                        "Class End Time:", TextBox("class_end"),
                        Button("Submit Class", "submit_course"), Button("Return to Homepage", "index")
                        ])

@route
def submit_course (state:State, class_name: str, class_start: str, class_end: str) -> Page:
    new_course = Course(class_name, Time(class_start, class_end))
    state.team.append(TeamMember(state.active_member, [new_course]))
    return Page(add_course)

@route
def group_availability (state: State) ->Page:
    return Page(state, ["Available the full time:",
                "Must leave early:",
                "Must arrive late:"])



@route
def index (state: State) -> Page:
    return Page(state, [Button("Add Team Member", "add_member"),
                        Button("Add Main Schedule", "add_to_main_schedule"),
                        Button("View Group Availability", "group_availability")])
