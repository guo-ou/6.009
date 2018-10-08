# NO IMPORTS!

#############
# Problem 1 #
#############

def count_viable(weights, capacity):
    """ Returns the number of viable sets of animals """
    new_weights = [w  for w in weights if w <= capacity]

    if not new_weights:
        return 1

    v1 = count_viable(new_weights[1:], capacity)
    v2 = count_viable(new_weights[1:], capacity - new_weights[0])

    return v1 + v2



#############
# Problem 2 #
#############

def find_valid_ordering(class_graph):
    """ Returns a valid ordering of classes """
    prereqs = dict()
    for course, clist in class_graph.items():
        for c in clist:
            if c not in prereqs:
                prereqs[c] = []
            prereqs[c].append(course)

    print(prereqs)
    clist = []

    def take(c):

        if c in clist:
            return

        else:
            output = []
            if c in prereqs:
                for subj in prereqs[c]:
                    take(subj)

            clist.append(c)

    for course in class_graph:
        take(course)

    return clist



#############
# Problem 3 #
#############

class Class_DB(object):
    def __init__(self):
        self.schedule = dict()

def build_rep(default_db, update_db):
    """ Returns a representation of the information in default_db and update_db.
        This representation will be used to implement the other methods."""
    # Default Representation
    # rep = [default_db, update_db] # CHANGE ME!

    ## Instantiate original class db
    output_DB = Class_DB()
    for entry in default_db:
        if entry[0] not in output_DB.schedule:
            output_DB.schedule[entry[0]] = []
            for i in range(15):
                output_DB.schedule[entry[0]].append(entry[1:] + [str(i + 1)])
        else:
            for i in range(15):
                output_DB.schedule[entry[0]].append(entry[1:] + [str(i + 1)])

    # print(output_DB.schedule)
    for entry in update_db:
        if entry[0] == "ADD":

            output_DB.schedule[entry[1]].append(entry[2:])

        if entry[0] == "DELETE":
            output_DB.schedule[entry[1]].remove(entry[2:])

    return output_DB


def get_class_days(class_list, rep):
    """ Returns a list of lists class_dates where class_dates[i] is a list of all
        dates on which class_list[i] meets """
    class_dates = []
    for i in range(len(class_list)):
        course_dates = []
        if class_list[i] not in rep.schedule:
            class_dates.append(course_dates)
            continue
        for section in rep.schedule[class_list[i]]:
            if section[1:][::-1] not in course_dates:
                course_dates.append(section[1:][::-1])
        class_dates.append(course_dates)

    return class_dates


def get_late_classes(time, rep):
    """ Returns a list of all classes that never meet before the specified time """
    output = []
    for course in rep.schedule:
        if all(int(section[0]) >= int(time) for section in rep.schedule[course]):
            output.append(course)


    return output


#############
# Problem 4 #
#############

class Student(object):
    def __init__(self, name, subjects):
        self.name = name
        self.subjects = subjects



class TermRecords(object):
    """Track subjects and students through the term."""

    def __init__(self,records):
        """Initialize term from list of records.

        Each record has the following form:
            {"student": student, "subjects": [subject, subject, ...]}
        """
        stud_recs = []

        for record in records:
            new_student = Student(record["student"], record["subjects"])
            stud_recs.append(new_student)

        self.students = stud_recs


        subject_dict = dict()
        for student in self.students:
            for course in student.subjects:
                if course not in subject_dict:
                    subject_dict[course] = [student.name]
                else:
                    subject_dict[course].append(student.name)

        self.registrations = subject_dict

    def __contains__(self, name):
        for student in self.students:
            if student.name == name:
                return True

        return False


    def transcript(self,student_id):
        """Return list of subjects for which student is registered."""
        for student in self.students:
            if student.name == student_id:
                return student.subjects

        return None

    def classlist(self,subject):
        """Return list of students registered for `subject`."""
        out_list = []
        for student in self.students:
            if subject in student.subjects:
                out_list.append(student.name)

        return out_list if out_list else None

    def add(self,student_id,subject):
        """Specified student has added a `subject`.

        Should also handle the following cases:
        -- student didn't exist before
        -- subject didn't exist before
        -- student was already registered for subject
        """
        if student_id in self:
            for student in self.students:
                if student.name == student_id:
                    if subject in student.subjects:
                        break
                    student.subjects.append(subject)
        else:
            self.students.append(Student(student_id, [subject]))

    def drop(self,student_id,subject):
        """Specified student has dropped a subject.

        Should also handle the following cases:
        -- student doesn't exist
        -- subject doesn't exist
        -- student wasn't registered for subject
        """
        if student_id in self:
            for student in self.students:
                if student.name == student_id:
                    if subject not in student.subjects:
                        break
                    student.subjects.remove(subject)

        else:
            pass

    def too_many_subjects(self,limit):
        """Return list of students registered for more than `limit` subjects."""
        output = []
        for student in self.students:
            if len(student.subjects) > limit:
                output.append(student.name)

        return output

    def enrollments(self):
        """Return list of (subject, # of registered students) for all subjects."""

        out_list = []
        for course, students in self.registrations.items():
            out_list.append([course, len(students)])

        return out_list


    def taking_all(self,subject_list):
        """Return list of students taking *all* of the listed subjects."""

        output = []
        for student in self.students:
            if set(student.subjects).issuperset(set(subject_list)) :
                output.append(student.name)

        return output

    def taking_some(self,subject_list):
        """Return list of students taking *at least one* of the listed subjects."""
        output = []
        for student in self.students:
            if set(student.subjects).intersection(set(subject_list)) != set() :
                output.append(student.name)

        return output

    def better_together(self,N):
        """Return count of students who have at least n subjects in
        common with at least one other student."""
        count = 0
        for student1 in self.students:
            for student2 in self.students:
                if student1 == student2:
                    continue

                if len(set(student1.subjects).intersection(set(student2.subjects))) >= N:
                    count += 1
                    break

        return count
#############
# Problem 5 #
#############

def has_liberty(board,row,col,seen=None):
    """Return ``True`` if stone at intersection (`row`, `col`) has
    at least one liberty or if there is no stone at the
    intersection, ''False'' if the stone has no liberties."""


    if seen is None:
        seen = set()


    if board[row][col] == ".":
        return True

    else:
        for ix in range(-1,2):
            for iy in range(-1,2):
                if not (ix == 0 or iy == 0):
                    continue

                if ix == iy:
                    continue

                if 0 <= row + ix < len(board) and 0 <= col + iy < len(board[0]) and board[row + ix][col + iy] in [board[row][col], "."]and (row + ix, col + iy) not in seen:
                    seen.add((row, col))

                    if has_liberty(board, row + ix, col + iy, seen):
                        return True

        return False


def capture(board,color):
    """Return updated `board` with all the captured stones of
    specified `color` removed."""
    outboard = []
    for r in range(len(board)):
        row = ""
        for c in range(len(board[0])):
            if not has_liberty(board, r, c) and board[r][c] == color:
                row += "."
            else:
                row += board[r][c]

        outboard.append(row)

    return outboard


# handy test board
board= [
  '.bwwb',
  'bbwwb',
  'bwb.w',
  'bbwbw',
  'wbwwb'
]


#############
# Problem 6 #
#############

def count_straights(k, L, n):
    """
    Count the possible hands in k-Label Poker where
      k = # labels
      L = # levels, 1...L inclusive
      n = number cards in a hand

    """
    def check_straights(hand):
        pass

    all_ops = set()

    ## L first options
    ## L - a second options
    ## L - a - b third options




#############
# Problem 7 #
#############

class Schedule_DB(object):
    def __init__(self):
        self.schedule = dict()

def build_schedule_rep(default_db, update_db):
    rep = Schedule_DB()
    for entry in default_db:

        if entry[0] not in rep.schedule:
            rep.schedule[entry[0]] = []

            for i in range(15):
                rep.schedule[entry[0]].append(entry[1:] + [str(i + 1)])
        else:
            for i in range(15):
                rep.schedule[entry[0]].append(entry[1:] + [str(i + 1)])


    for entry in update_db:
        if entry[0] == "ADD":
            rep.schedule[entry[1]].append(entry[2:])

        elif entry[0] == "DELETE":
            rep.schedule[entry[1]].remove(entry[2:])

    return rep

def get_near_classes(buildings, rep):
    """
    OUTPUT: A list, in no particular order, of all classes that meet
    only in the list of buildings given by `buildings`.
    """
    output = []
    for course, data in rep.schedule.items():
        if all(section[2] in buildings for section in data):
            output.append(course)
    return output

def earliest_meeting(building, day_of_week, rep):
    """
    OUTPUT: An integer earliest time (hour, such as 9),
    the earliest meeting given by the combined database of classes,
    occurring on any week in `building` on `day_of_week`.
    If no meetings take place on `day_of_week` in that building on any
     week, return `None`.
    """
    earliest = "25"

    for course, data in rep.schedule.items():
        for section in data:

            if section[2] != building or section[1] != day_of_week:
                continue

            if int(section[0]) < int(earliest):
                earliest = section[0]

    if earliest == "25":
        return None

    return int(earliest)





def have_conflicts(class_list, rep):
    """
    OUTPUT: A Boolean (True/False) indicating whether any two classes
    in class_list conflict. Two classes conflict when they meet on the same day
    of the week during the same week at the same time.
    """

    for course1 in class_list:
        if course1 not in rep.schedule:
            continue

        for course2 in class_list:

            if course1 == course2:
                continue

            if course2 not in rep.schedule:
                continue

            for sec1 in rep.schedule[course1]:
                for sec2 in rep.schedule[course2]:

                    if sec1[0] == sec2[0] and sec1[1] == sec2[1] and sec1[3] == sec2[3]:
                        return True

    return False
