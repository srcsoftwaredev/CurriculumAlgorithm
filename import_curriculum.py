import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'CurriculumAlgorithmWebApp.settings'
django.setup()
from curriculum_algorithm.models import CurriculumCourse, Course
from curriculum_algorithm.models import Curriculum


def import_curriculum(name):
    file = open(name + '.txt', 'r')
    curriculum = Curriculum.objects.create(name=name)
    for line in file:
        line = line.split()
        print(line)
        course = CurriculumCourse.objects.create(curriculum=curriculum, course=Course.objects.create(course_number=line[0], credit_hours=int(line[1])))
        if line[2] != '--------':
            courses = line[2].split(',')
            for correq in courses:
                course.co_requisites.add(CurriculumCourse.objects.filter(course__course_number=correq, curriculum=curriculum).first())
        if line[3] != '--------':
            courses = line[3].split(',')
            for prereq in courses:
                course.add_pre_requisite(CurriculumCourse.objects.filter(course__course_number=prereq, curriculum=curriculum).first())
        if line[4] != '--------':
            lab = CurriculumCourse.objects.create(curriculum=curriculum, course=Course.objects.create(course_number=line[4], credit_hours=1))
            course.laboratory = lab
        if line[5] != '--------':
            course.season = int(line[5][-1])
        course.save()

    return curriculum


if __name__ == '__main__':
    import_curriculum('CIIC')