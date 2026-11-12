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
def submit_member (state: State, member_name:str) -> Page:
    state.active_member = member_name
    return add_course(state)

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
    return add_course(state)

@route
def group_availability (state: State) ->Page:
    return Page(state, ["Available the full time:",
                "Must leave early:",
                "Must arrive late:"])

@route
def add_to_main_schedule (state: State) -> Page:
    return Page(state, ["Activity Name:", TextBox("activity_name"),
                        "Activity Start Time:", TextBox("activity_start"),
                        "Activity End Time:", TextBox("activity_end"),
                        Button("Submit Activity", "submit_activity"), Button("Return to Homepage", "index")
                        ])

@route
def submit_activity (state:State, activity_name: str, activity_start: str, activity_end: str) -> Page:
    new_activity = Activity(activity_name, Time(activity_start, activity_end))
    state.main_schedule.append(Activity(new_activity))
    return add_to_main_schedule(state)


@route
def index (state: State) -> Page:
    return Page(state, [Button("Add Team Member", "add_member"),
                        Button("Add Main Schedule", "add_to_main_schedule"),
                        Button("View Group Availability", "group_availability")])
        
start_server(State([],[],""))
