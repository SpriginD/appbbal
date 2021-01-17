from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import JsonResponse

from QuizApp.models import Student, QuizMark

# Create your views here.

def index(request):
    students = get_list_or_404(Student.objects.order_by('student_number'))
    context = {'students': students}
    
    return render(request, 'QuizApp/index.html', context=context)

def student_results(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    quizzes = student.quizmark_set.all()
    quiz_names= ['Birinci Quiz', 'İkinci Quiz', 'Üçüncü Quiz', 'Dördüncü Quiz']
    disable_quizzes = list(range(len(quizzes), 4))

    context = {'student': student, 'quizzes': quizzes, 'quiz_names': quiz_names, 'disable_quizzes': disable_quizzes}

    return render(request, 'QuizApp/detail.html', context=context)

def quizzes_chart(request, std_id, quiz_id):
    student = get_object_or_404(Student, pk=std_id)
    quiz = student.quizmark_set.all()[int(quiz_id)-1]

    return JsonResponse(
        data = quiz.get_info()
    )

def avarage_quizzes_chart(request, quiz_id):
    students = get_list_or_404(Student.objects.order_by('student_number'))

    students_data = [student.get_marks()[int(quiz_id)-1] if len(student.get_marks())>=int(quiz_id) else 0 for student in students]
    students_labels = [std.get_full_name() for std in students]

    return JsonResponse(
        data = {
            'students_labels': students_labels,
            'students_data': students_data
        }
    )