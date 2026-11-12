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
    active_member: TeamMember

def string_of_team_members (state:State) -> str:
    team_members = ""
    for member in state.team:
        team_members = team_members + member.name + ": "
        for course in member.courses:
            team_members = team_members + course.name + " "
    return team_members
assert_equal(string_of_team_members(State([TeamMember("Geneva", [Course("CISC 108", Time("3:00", "3:55"))]),
                                           TeamMember("Abby", [Course("INTR 101", Time("000", "000")), Course("HONR", Time("000", "000"))]),
                                           TeamMember("Ava", [Course("BLAH", Time("000", "000"))])],
                                          [], "")), "Geneva: CISC 108 Abby: INTR 101 HONR Ava: BLAH ")

@route
def add_member (state: State) -> Page:
    return Page(state, ["Enter Full Name:", TextBox("member_name"),
                        Button("Submit Name", "submit_member"),
                        Button ("Return to Homepage", "index")])
    
@route
def submit_member (state: State, member_name:str) -> Page:
    state.active_member = TeamMember(member_name, [])
    return submitted_name(state)
@route
def submitted_name (state:State) -> Page:
    return Page(state, ["Name Submitted!", "\n", Button("Now Add Class", "add_course")])

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
    course_added_to_active_member = state.active_member.courses.append(new_course)
    state.team.append(course_added_to_active_member)
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
    state.main_schedule.append(new_activity)
    return add_to_main_schedule(state)


@route
def view_team_members (state: State) -> Page:
    return Page(state, ["Team Members:", string_of_team_members(state)])

@route
def index (state: State) -> Page:
    return Page(state, [Button("Add Team Member", "add_member"),
                        Button("Add Main Schedule", "add_to_main_schedule"),
                        Button("View Group Availability", "group_availability"),
                        Button("View Team Members", "view_team_members")])
        
start_server(State([],[],""))
