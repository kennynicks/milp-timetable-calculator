#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pulp import *
from tabulate import tabulate
import itertools


################## INPUT DATA ##################

# Tage
days_cleartext = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
days = range(len(days_cleartext))

# Slots
slots_cleartext = ["1.", "2.", "3.", "4.", "5.", "6."]
slots = range(len(slots_cleartext))

# Klassen
classes_cleartext = ["1a", "1b", "2a", "2b", "3a", "3b", "4a", "4b", "Fö"]
classes = range(len(classes_cleartext))

# Fächer
categories_cleartext = ["Sonstiges", "Englisch", "Förder"]
categories = range(len(categories_cleartext))

# Lehrer
teachers_cleartext = ["Wa", "Ka", "SB", "Si", "KE",
                      "Ba", "Ma", "Oc", "Gr", "Kl", "Ku", "Him"]
teachers = range(len(teachers_cleartext))
remedial_teacher = 10

teacherCategories = [
    [0], [0], [0], [0],
    [0], [0], [0], [0],
    [0], [0], [0], [0, 1]
]
teacherCategories[remedial_teacher].append(2)

class_categories = {
    (0, 0): 23,
    (0, 1): 2,
    (0, 2): 0,
    (1, 0): 23,
    (1, 1): 2,
    (1, 2): 0,
    (2, 0): 23,
    (2, 1): 2,
    (2, 2): 0,
    (3, 0): 23,
    (3, 1): 2,
    (3, 2): 0,
    (4, 0): 23,
    (4, 1): 2,
    (4, 2): 0,
    (5, 0): 23,
    (5, 1): 2,
    (5, 2): 0,
    (6, 0): 25,
    (6, 1): 0,
    (6, 2): 0,
    (7, 0): 25,
    (7, 1): 0,
    (7, 2): 0,
    (8, 0): 0,
    (8, 1): 0,
    (8, 2): 10
}

teacherLessons = [
    18, 14, 14, 28,
    19, 22, 24, 24,
    27, 26, 28, 23
]

classTeachers = {
    0: (0,),
    1: (1, 2),
    2: (3,),
    3: (4,),
    4: (5,),
    5: (6,),
    6: (7,),
    7: (8,),
    8: (remedial_teacher,)
}

classTeacherNames = [", ".join(map(lambda x: teachers_cleartext[x],
                                   classTeachers[clazz])) for clazz in classes]

teacherCombinations = list(itertools.combinations(
    teachers, 1)) + list(itertools.combinations(teachers, 2))
teacherCategoryCombinations = []
for combination in teacherCombinations:
    categories = list(set(itertools.chain.from_iterable(
        [teacherCategories[teacher] for teacher in combination])))
    for category in categories:
        if category == 2 and len(combination) == 2:
            continue
        teacherCategoryCombinations.append({
            "teachers": combination,
            "category": category
        })

lessons = range(len(teacherCategoryCombinations))

slot_combinations = {
    0: [0, 0, 0, 0, 0, 0],
    1: [1, 0, 0, 0, 0, 0],
    2: [0, 1, 0, 0, 0, 0],
    3: [0, 0, 1, 0, 0, 0],
    4: [0, 0, 0, 1, 0, 0],
    5: [0, 0, 0, 0, 1, 0],
    6: [0, 0, 0, 0, 0, 1],
    7: [1, 1, 0, 0, 0, 0],
    8: [0, 1, 1, 0, 0, 0],
    9: [0, 0, 1, 1, 0, 0],
    10: [0, 0, 0, 1, 1, 0],
    11: [0, 0, 0, 0, 1, 1],
    12: [1, 1, 1, 0, 0, 0],
    13: [0, 1, 1, 1, 0, 0],
    14: [0, 0, 1, 1, 1, 0],
    15: [0, 0, 0, 1, 1, 1],
    16: [1, 1, 1, 1, 0, 0],
    17: [0, 1, 1, 1, 1, 0],
    18: [0, 0, 1, 1, 1, 1],
    19: [1, 1, 1, 1, 1, 0],
    20: [0, 1, 1, 1, 1, 1],
    21: [1, 1, 1, 1, 1, 1],
}

last_slot_to_slot_combinations = {
    -1: (0,),
    0: (1,),
    1: (2, 7,),
    2: (3, 8, 12,),
    3: (4, 9, 13, 16,),
    4: (5, 10, 14, 17, 19,),
    5: (6, 11, 15, 18, 20, 21,),
}


school_end_slots = [-1, *slots]


n_slot_combinations = range(len(slot_combinations))

grade_levels = {
    0: (0, 1,),
    1: (2, 3,),
    2: (4, 5,),
    3: (6, 7,)
}

grade_levels_clear_text = {
    0: "erste",
    1: "zweite",
    2: "dritte",
    3: "vierte"
}

n_grade_levels = range(len(grade_levels))
################################################

##################  VARIABLES  ##########################
p_school_end_deviation = {
    (day, grade_level): LpVariable("Stundenabweichung der Stufe %s am %s" %
                                   (grade_levels_clear_text[grade_level], days_cleartext[day]), cat=LpInteger, lowBound=0)
    for grade_level in n_grade_levels
    for day in days
}

class_teached_by = {
    (clazz, teacher): LpVariable("Klasse %s wird in der Woche von %s unterrichtet"
                                 % (classes_cleartext[clazz],
                                    teachers_cleartext[teacher],
                                    ), cat=LpBinary)
    for clazz in classes
    for teacher in teachers
}

teacher_day_slot_combination = {
    (teacher, day, slot_combination): LpVariable("Am Tag %s hat Lehrer %s die Stunden-Kombination %s"
                                                 % (days_cleartext[day],
                                                    teachers_cleartext[teacher],
                                                    slot_combination,
                                                    ), cat=LpBinary)
    for day in days
    for teacher in teachers
    for slot_combination in n_slot_combinations
}

x = {
    (day, slot, clazz, lesson): LpVariable("Am %s in der %s Stunde wird in der Klasse %s %s von %s unterrichtet"
                                           % (days_cleartext[day],
                                              slots_cleartext[slot],
                                              classes_cleartext[clazz],
                                              teacherCategoryCombinations[lesson]["category"],
                                              teacherCategoryCombinations[lesson]["teachers"]
                                              ), cat=LpBinary)
    for day in days
    for slot in slots
    for clazz in classes
    for lesson in lessons
}

slot_used = {
    (day, slot, clazz): LpVariable("Am Tag %s in der Klasse %s wird in der %s Stunde unterrichtet"
                                   % (days_cleartext[day],
                                      classes_cleartext[clazz],
                                      slots_cleartext[slot],
                                      ), cat=LpBinary)
    for day in days
    for slot in slots
    for clazz in classes
}

teacher_school_end = {
    (teacher, day, school_end_slot): LpVariable("Am %s hat %s ab Slot %s frei"
                                                % (days_cleartext[day], teachers_cleartext[teacher], school_end_slot), cat=LpBinary)
    for day in days
    for teacher in teachers
    for school_end_slot in school_end_slots
}

same_day_school_end = {
    (day, school_end_slot): LpVariable("Am %s haben alle ab der %s Stunde schluss" % (days_cleartext[day], school_end_slot), cat=LpBinary,)
    for day in days
    for school_end_slot in school_end_slots
}

teacher_day_ogs = {
    (teacher, day): LpVariable("%s hat am %s OGS" % (teachers_cleartext[teacher], days_cleartext[day]), cat=LpBinary)
    for teacher in teachers
    for day in days
}

# teacher_day_remedial_slot = {
#     (teacher, day, slot): LpVariable("%s hat am %s in der %s Stunde Förderunterricht" % (teacher, day, slot), cat=LpBinary)
#     for teacher in teachers
#     for day in days
#     for slot in slots
# }

#########################################################

problem = LpProblem("Stundenplan", sense=LpMaximize)


##################  CONSTRAINTS  ########################

# * Jede Klasse hat max n stunden aus kategorie c pro Woche
for clazz in classes:
    for category in categories:
        problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                                    for day in days
                                    for slot in slots
                                    for lesson in lessons
                                    if teacherCategoryCombinations[lesson]["category"] == category
                                    ) == class_categories[clazz, category])

# * Jede klasse hat im slot 0 jeden tages unterricht
for day in days:
    for clazz in classes[:-1]:
        problem.addConstraint(
            lpSum(x[(day, 0, clazz, lesson)] for lesson in lessons) == 1)

# * Jeder Lehrer darf an jedem Tag in jedem Slot nur eine Klasse unterrichten
for teacher in teachers:
    for day in days:
        for slot in slots:
            problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                                        for clazz in classes
                                        for lesson in lessons
                                        if teacher in teacherCategoryCombinations[lesson]["teachers"]
                                        ) == lpSum(
                teacher_day_slot_combination[(teacher, day, combination)] * slot_combinations[combination][slot] for
                combination in n_slot_combinations))

# * An jedem Tag hat jede Klasse maximal eine Stunde englisch
for day in days:
    for clazz in classes[:-1]:
        problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                              for slot in slots for lesson in lessons if teacherCategoryCombinations[lesson]["category"] == 1) <= 1)


# * Für jeden Slot darf nur eine Combination ausgewählt sein
for day in days:
    for slot in slots:
        for clazz in classes:
            problem.addConstraint(
                lpSum(x[(day, slot, clazz, lesson)] for lesson in lessons) == 1 * slot_used[(day, slot, clazz)])

# * Jeder Lehrer darf nur eine bestimmte Stundenzahl pro Woche unterrichten
for teacher in teachers:
    problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                                for day in days
                                for slot in slots
                                for clazz in classes
                                for lesson in lessons
                                if teacher in teacherCategoryCombinations[lesson]["teachers"]
                                )
                          + lpSum(teacher_day_ogs[(teacher, day)]
                                  for day in days)
                          == teacherLessons[teacher])

# * Alle Klassenstufen haben paarweise gleichzeitig schluss (1a+1b gleichzeitig!) => kann muss aber nicht
for grade_level in n_grade_levels:
    for day in days:
        for clazz in grade_levels[grade_level][:-1]:
            problem.addConstraint((lpSum(x[(day, slot, clazz, lesson)]
                                         for lesson in lessons
                                         for slot in slots)-lpSum(
                x[(day, slot, clazz+1, lesson)]
                for lesson in lessons
                for slot in slots)) == p_school_end_deviation[(day, grade_level)])

# * Keine FREISTUNDEN
for day in days:
    for clazz in classes[:-1]:
        for slot in slots[:-1]:
            problem.addConstraint(
                slot_used[(day, slot, clazz)] - slot_used[(day, slot + 1, clazz)] >= 0)

# * Alle Lehrer haben mindestens einmal die Woche gleichzeitig Schluss => muss (am besten Montags)
for teacher in teachers:
    for day in days:
        for school_end_slot in school_end_slots:
            problem.addConstraint(teacher_school_end[(
                teacher, day, school_end_slot)] ==
                lpSum(teacher_day_slot_combination[(teacher, day, slot_combination)] for slot_combination in last_slot_to_slot_combinations[school_end_slot]))

for day in days:
    for school_end_slot in school_end_slots:
        problem.addConstraint((lpSum(teacher_school_end[(teacher, day, school_end_slot)] for teacher in teachers) - (len(
            teachers)-lpSum(teacher_school_end[(teacher, day, -1)]for teacher in teachers)))*-1 <= 13*(1-same_day_school_end[(day, school_end_slot)]))

for day in days:
    problem.addConstraint(lpSum(same_day_school_end[(
        day, school_end_slot)] for school_end_slot in school_end_slots) <= 1)

# todo einkommentieren
# montags
# problem.addConstraint(lpSum(same_day_school_end[(
#     0, school_end_slot)] for school_end_slot in school_end_slots ) >= 1)


# nicht zwingend aber höchst wünschenswert
# * keine SPRINGSTUNDEN
for teacher in teachers:
    for day in days:
        problem.addConstraint(lpSum(teacher_day_slot_combination[(
            teacher, day, slot_combination)] for slot_combination in n_slot_combinations) == 1)

# * Minimum 4h / Tag
for day in days:
    for clazz in classes[:-1]:
        problem.addConstraint(
            lpSum(slot_used[(day, slot, clazz)] for slot in slots) >= 4)

for clazz in classes:
    for teacher in teachers:
        problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                                    for day in days
                                    for slot in slots
                                    for lesson in lessons
                                    if teacher in teacherCategoryCombinations[lesson]["teachers"]
                                    ) <= 29 * class_teached_by[(clazz, teacher)])

# nicht zwingend aber höchst wünschenswert (möglichst nicht 1./2.)
# * Jede Klasse hat maximal drei Lehrkräfte
for clazz in classes:
    problem.addConstraint(
        lpSum(class_teached_by[(clazz, teacher)] for teacher in teachers) <= 3)

# * Die Klassenleitung hat mindestens 2 Stunden pro Tag in seiner Klasse
for clazz in classes:
    for day in days:
        problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                                    for lesson in lessons
                                    for slot in slots
                                    for teacher in teacherCategoryCombinations[lesson]["teachers"]
                                    if teacher in classTeachers[clazz]) >= 2)

# * OGS => 3 Lehrer opfern jeweils eine Stunde die Woche für OGS (anschluss an die 6. Stunde 14-15uhr) keine springstunde
# genau drei mal ogs
problem.addConstraint(lpSum(
    teacher_day_ogs[(teacher, day)] for teacher in teachers for day in days) == 3)
# jeder lehrer maximal einmal ogs
for teacher in teachers:
    problem.addConstraint(
        lpSum(teacher_day_ogs[(teacher, day)] for day in days) <= 1)
# an jedem tag maxinmal einmal ogs
for day in days:
    problem.addConstraint(
        lpSum(teacher_day_ogs[(teacher, day)] for teacher in teachers) <= 1)

problem.addConstraint(lpSum(teacher_day_ogs[(
    teacher, 0)] for teacher in teachers) == 0)  # montags keine ogs

# im anschluss an die sechste klasse
for teacher in teachers:
    for day in days:
        problem.addConstraint(
            teacher_day_ogs[(teacher, day)] <= teacher_school_end[(teacher, day, 5)])

# * förder: 2 stunden 4-5 mal die woche migrationskinder; möglichst alle klassen unterricht (muss aber nicht); Ein Lehrer
for day in days:
    # zwei stunden am tag förderunterricht
    problem.addConstraint(
        lpSum(slot_used[(day, slot, 8)] for slot in slots) == 2)
    # förderunterricht nur in der 1.-4. Stunde
    problem.addConstraint(lpSum(slot_used[(day, 4, 8)]) == 0)
    # förderunterricht nur in der 1.-4. Stunde
    problem.addConstraint(lpSum(slot_used[(day, 5, 8)]) == 0)


########################################################


#################  OBJECTIVE  ##################

# Maximize teacher hours in main class
problem.setObjective(lpSum(x[(day, slot, clazz, lesson)]
                           for day in days
                           for slot in slots
                           for clazz in classes
                           for lesson in lessons
                           for teacher in teacherCategoryCombinations[lesson]["teachers"]
                           if teacher in classTeachers[clazz]
                           )-lpSum(p_school_end_deviation[(day, grade_level)]
                                   for grade_level in n_grade_levels
                                   for day in days))

################################################
# The problem is solved using PuLP's choice of Solver
print("Constraints: %s" % (len(problem.constraints)))
problem.solve(GUROBI_CMD())

#################  OUTPUT  ##################

# The status of the solution is printed to the screen
print("Status:", LpStatus[problem.status])
day_data = {}
for day in days:
    day_data[day] = []

for day in days:
    for slot in slots:
        slot_data = [slots_cleartext[slot]]
        day_data[day].append(slot_data)
        for clazz in classes:
            if sum(value(x[(day, slot, clazz, lesson)]) for lesson in lessons) == 0:
                slot_data.append("-")
                continue

            for lesson in lessons:
                if value(x[(day, slot, clazz, lesson)]) == 0:
                    continue
                fach = {0: "", 1: " 'E'", 2: " 'FÖ'"}
                slot_data.append(", ".join(list(map(
                    lambda x: teachers_cleartext[x], teacherCategoryCombinations[lesson]["teachers"]))) + fach[
                    teacherCategoryCombinations[lesson]["category"]])
    day_data[day].append(["7."])
    teacher_ogs_data = ["8."]
    for teacher in teachers:
        if value(teacher_day_ogs[(teacher, day)]) == 1:
            teacher_ogs_data.append("OGS von %s" %
                                    (teachers_cleartext[teacher]))
    day_data[day].append(teacher_ogs_data)

for day in days:
    print()
    print(days_cleartext[day] + ":")
    print(tabulate(day_data[day], headers=[
        "Stunde", *["%s - %s" % x for x in zip(classes_cleartext, classTeacherNames)]]))

print()
for day in days:
    if sum(value(same_day_school_end[(day, school_end_slot)])for school_end_slot in school_end_slots) == 1:
        print("Gemeinsam Schluss am %s" % (days_cleartext[day]))
#############################################
# TODO gewichtung doppelbesetzungen => vorallem 1./2.
# TODO persönliche präferenzen
# TODO religion am ende des tages => muss
# TODO schwimmen MUSS in doppelbesetzung
# TODO sport und religion KEINE doppelbesetzung
# TODO fixe schwimmzeiten
# TODO teils fixe sportzeiten (mehrere Klassen gleichzeitig => zwei hallen 3./4.)
# TODO fächer: sport [alle], schwimmen, englisch, religion [1./2. alle sonst nicht alle]
# TODO sport in der 3. und 4. muss Doppelstunde sein (1./2. ist egal)
