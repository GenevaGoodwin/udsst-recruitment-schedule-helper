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
class Availability:
    activity_name: str
    team_availability: list[str]
@dataclass
class State:
    team: list[TeamMember]
    activities: list[Activity]
    active_member: TeamMember
    team_availability: list[Availability]
    
def time_checker (time: str) -> bool:
    if len(time) == 5:
        if time[0:2].isdigit() and time[2:3] == ":" and time[3:5].isdigit():
            return True
    else:
        return False
def single_activity_availability_checker (activity: Activity, team_member:TeamMember) -> str:
    available = True
    if not team_member.courses:
        return team_member.name 
    for course in team_member.courses:
        if course.time.start < activity.time.start and course.time.end < activity.time.start:
            available = True
        elif course.time.start > activity.time.end and course.time.end > activity.time.end:
            available = True
        elif course.time.start >= activity.time.start and course.time.start < activity.time.end:
            return team_member.name + " must leave early."
        elif course.time.start < activity.time.start and course.time.end > activity.time.start:
            return team_member.name + " must arrive late."
        elif course.time.start < activity.time.start and course.time.end > activity.time.end:
            return team_member.name + " must miss the entire activity."
        elif course.time.start >= activity.time.start and course.time.end <= activty.time.end:
            return "Probably has to miss entire activity, but talk to " + team_member.name
    return team_member.name + " is available!"
            
def activity_checker (state: State) -> list[Availability]:
    current_team_availability = ""
    if not state.team:
        return []
    if not state.activities:
        return []
    for activity in state.activities:
        current_team_availability = ""
        for team_member in state.team:
            current_team_availability = single_activity_availability_checker(activity, team_member) + current_team_availability
        state.team_availability.append(Availability(activity.name, current_team_availability))
    return state.team_availability
#assert_equal(activity_checker(State(
def parse_team_availabilities (team_availabilities: list[Availability]) -> str:
    total_availability_str = ""
    availability_str = ""
    if not team_availabilities:
        return "Error: No availability found."
    for availability in team_availabilities:
        availability_str = availability.activity_name + ":" 
        for team_member_availability in availability.team_availability:
            availability_str = availability_str + team_member_availability
        total_availability_str = total_availability_str + availability_str.rstrip(",") + "\n"
    return total_availability_str

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
                                          [], "", [])), "Geneva: CISC 108 Abby: INTR 101 HONR Ava: BLAH ")


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
                        "Class Start Time (24 hour clock):", TextBox("class_start"),
                        "Class End Time(24 hour clock):", TextBox("class_end"),
                        Button("Submit Class", "submit_course"),
                        Button("Return to Homepage", "index")
                        ])
@route
def user_error (state: State) -> Page:
    return Page(state, ["FORMAT ERROR: Please check your start and end time and make sure they are in military time.",
                        "\n", "For example 2:00 pm should be 14:00, 8:00 am should be 08:00.", "\n",
                        "Class Name:", TextBox("class_name"),
                        "Class Start Time (24 hour clock):", TextBox("class_start"),
                        "Class End Time(24 hour clock):", TextBox("class_end"),
                        Button("Submit Class", "submit_course"),
                        Button("Return to Homepage", "index")
                        ])


@route
def submit_course (state:State, class_name: str, class_start: str, class_end: str) -> Page:
    new_course = Course(class_name, Time(class_start, class_end))
    state.active_member.courses.append(new_course)
    if state.active_member not in state.team:
        state.team.append(state.active_member)
    if time_checker(class_start) and time_checker(class_end):
        return add_course(state)
    else:
        return user_error(state)

@route
def group_availability (state: State) ->Page:
    return Page(state, [parse_team_availabilities(activity_checker(state)),
                Button("Return to Homepage", "index")
                        ])

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
    state.activities.append(new_activity)
    return add_to_main_schedule(state)


@route
def view_team_members (state: State) -> Page:
    return Page(state, ["Team Members:", string_of_team_members(state), "\n", Button("Return to Homepage", "index")])

@route
def index (state: State) -> Page:
    return Page(state, [Button("Add Team Member", "add_member"),
                        Button("Add Main Schedule", "add_to_main_schedule"),
                        Button("View Group Availability", "group_availability"),
                        Button("View Team Members", "view_team_members")])
        
start_server(State([],[],"",[]))
