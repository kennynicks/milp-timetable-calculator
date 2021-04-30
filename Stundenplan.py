#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pulp import *
from tabulate import tabulate
import itertools

# Tage
days_cleartext = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
days = range(len(days_cleartext))

# Slots
slots_cleartext = ["1.", "2.", "3.", "4.", "5.", "6."]
slots = range(len(slots_cleartext))

# Klassen
classes_cleartext = ["1a", "1b", "2a", "2b", "3a", "3b", "4a", "4b"]
classes = range(len(classes_cleartext))

# Fächer
categories_cleartext = ["Sonstiges", "Englisch"]
categories = range(len(categories_cleartext))

# Lehrer
teachers_cleartext = ["Wa", "Ka", "SB", "Si", "KE",
                      "Ba", "Ma", "Oc", "Gr", "Kl", "Ku", "Him"]
teachers = range(len(teachers_cleartext))

teacherCategories = [
    [0], [0], [0], [0],
    [0], [0], [0], [0],
    [0], [0], [0], [0, 1]
]

class_categories = {
    (0, 0): 23,
    (0, 1): 2,
    (1, 0): 23,
    (1, 1): 2,
    (2, 0): 23,
    (2, 1): 2,
    (3, 0): 23,
    (3, 1): 2,
    (4, 0): 23,
    (4, 1): 2,
    (5, 0): 23,
    (5, 1): 2,
    (6, 0): 25,
    (6, 1): 0,
    (7, 0): 25,
    (7, 1): 0
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
    7: (8,)
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
        teacherCategoryCombinations.append({
            "teachers": combination,
            "category": category
        })

lessons = range(len(teacherCategoryCombinations))

problem = LpProblem("Stundenplan", sense=LpMaximize)

##############

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

n_slot_combinations = range(len(slot_combinations))

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

class_teached_by = {
    (clazz, teacher): LpVariable("Klasse %s wird in der Woche von %s unterrichtet"
                                 % (classes_cleartext[clazz],
                                    teachers_cleartext[teacher],
                                    ), cat=LpBinary)
    for clazz in classes
    for teacher in teachers
}

# Jede Klasse hat max n stunden aus kategorie c pro Woche
for clazz in classes:
    for category in categories:
        problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                                    for day in days
                                    for slot in slots
                                    for lesson in lessons
                                    if teacherCategoryCombinations[lesson]["category"] == category
                                    ) == class_categories[clazz, category])

# Jede klasse hat im slot 0 jeden tages unterricht
for day in days:
    for clazz in classes:
        problem.addConstraint(
            lpSum(x[(day, 0, clazz, lesson)] for lesson in lessons) == 1)

# Jeder Lehrer darf an jedem Tag in jedem Slot nur eine Klasse unterrichten
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

# Für jeden Slot darf nur eine Combination ausgewählt sein
for day in days:
    for slot in slots:
        for clazz in classes:
            problem.addConstraint(
                lpSum(x[(day, slot, clazz, lesson)] for lesson in lessons) == 1 * slot_used[(day, slot, clazz)])

# Jeder Lehrer darf nur eine bestimmte Stundenzahl pro Woche unterrichten
for teacher in teachers:
    problem.addConstraint(lpSum(x[(day, slot, clazz, lesson)]
                                for day in days
                                for slot in slots
                                for clazz in classes
                                for lesson in lessons
                                if teacher in teacherCategoryCombinations[lesson]["teachers"]
                                ) == teacherLessons[teacher])

#TODO Klassenstufen gleichzeitig schluss (1a+1b gleichzeitig!) => kann muss aber nicht

# Keine FREISTUNDEN
for day in days:
    for clazz in classes:
        for slot in slots[:-1]:
            problem.addConstraint(
                slot_used[(day, slot, clazz)] - slot_used[(day, slot + 1, clazz)] >= 0)

#TODO nicht zwingend aber höchst wünschenswert
# keine SPRINGSTUNDEN
for teacher in teachers:
    for day in days:
        problem.addConstraint(lpSum(teacher_day_slot_combination[(
            teacher, day, slot_combination)] for slot_combination in n_slot_combinations) == 1)

# Minimum 4h / Tag
for day in days:
    for clazz in classes:
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

#TODO nicht zwingend aber höchst wünschenswert (möglichst nicht 1./2.)
# Jede Klasse hat maximal drei Lehrkräfte
for clazz in classes:
    problem.addConstraint(lpSum(class_teached_by[(clazz, teacher)] for teacher in teachers) <= 3)

# Maximize teacher hours in main class
problem.setObjective(lpSum(x[(day, slot, clazz, lesson)]
                           for day in days
                           for slot in slots
                           for clazz in classes
                           for lesson in lessons
                           for teacher in teacherCategoryCombinations[lesson]["teachers"]
                           if teacher in classTeachers[clazz]
                           ))

# The problem is solved using PuLP's choice of Solver
problem.solve(GUROBI_CMD())

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
                fach = {0: "", 1: " 'E'"}
                slot_data.append(", ".join(list(map(
                    lambda x: teachers_cleartext[x], teacherCategoryCombinations[lesson]["teachers"]))) + fach[
                                     teacherCategoryCombinations[lesson]["category"]])

for day in days:
    print()
    print(days_cleartext[day] + ":")
    print(tabulate(day_data[day], headers=[
        "Stunde", *["%s - %s" % x for x in zip(classes_cleartext, classTeacherNames)]]))

teacher_hours = []
for teacher in teachers:
    hours = sum(value(x[(day, slot, clazz, lesson)])
                for day in days
                for slot in slots
                for clazz in classes
                for lesson in lessons
                if teacher in teacherCategoryCombinations[lesson]["teachers"]
                )
    teacher_hours.append([teachers_cleartext[teacher], teacherLessons[teacher],
                          hours, hours - teacherLessons[teacher]])

#TODO persönliche präferenzen
#TODO religion am ende des tages => muss
#TODO schwimmen MUSS in doppelbesetzung
#TODO sport und religion KEINE doppelbesetzung
#TODO einmal in der woche alle lehrer gleichzeitig schluss => muss (montag)
#TODO fixe schwimmzeiten
#TODO teils fixe sportzeiten (mehrere Klassen gleichzeitig => zwei hallen 3./4.)
#TODO fächer: sport [alle], schwimmen, englisch, religion [1./2. alle sonst nicht alle]
#TODO gewichtung doppelbesetzungen => vorallem 1./2.
#TODO OGS => 3 Lehrer opfern jeweils eine Stunde die Woche für OGS (anschluss an die 6. Stunde 14-15uhr) keine springstunde
#TODO förder: 2st jeder tag migrationskinder; möglichst alle klassen unterricht (muss aber nicht)
#TODO [russ/türk: max 2 stufen. am besten 2; teilweise parallel zum unterricht]
