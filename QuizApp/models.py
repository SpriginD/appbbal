from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import localdate
# import locale

# Locale config
# locale.setlocale(locale.LC_ALL, "tr_TR.utf8")

# Create your models here.

class Student(models.Model):
    student_name = models.CharField(max_length=30)
    student_surname = models.CharField(max_length=30)
    student_number = models.IntegerField()

    def get_marks(self):
        return [quiz.mark for quiz in self.quizmark_set.all()]

    def get_avarage(self):
        marks = self.get_marks()
        if len(marks) != 0:
            result = (sum(marks) / len(marks))
        else:
            result = "Henüz girilmiş quiz yok."
        return result
    
    def get_last_date(self):
        last_mark_date = self.quizmark_set.last().last_date if self.quizmark_set.last() else localdate()
        delta_day = (localdate()-last_mark_date).days

        first_section = "{day} gün önce güncellendi".format(day=delta_day) if delta_day > 0 else "Bügün güncellendi"
        second_section = last_mark_date.strftime("%d/%m/%Y")
        third_section = last_mark_date.strftime("%A")

        dates_data = " | ".join([first_section, second_section, third_section])
        return dates_data


    def get_full_name(self):
        full_name = "{name} {surname}".format(
            name = self.student_name,
            surname = self.student_surname
        )

        return full_name

    def set_state(self):
        mark_length = len(self.get_marks())
        mark_count = {1: 'tek', 2: 'iki', 3: 'üç', 4: 'dört', 5: 'beş'}

        if mark_length == 0:
            state = "Henüz girilmiş quiziniz bulunmamaktadır."
        else:
            state = "Mevcut girilmiş {count} quiziniz bulunmaktadır.".format(count = mark_count[mark_length])

        return state

    def __str__(self):
        title = self.get_full_name()

        return title

    class Meta:
        ordering = ['student_name', 'student_surname', 'student_number']


class QuizMark(models.Model):
    first  = '1'
    second = '2'
    third  = '3'
    fourth = '4'

    WHICH_CHOICES = [
        (first, 'Birinci'),
        (second, 'İkinci'),
        (third, 'Üçüncü'),
        (fourth, 'Dördüncü')
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    which_quiz = models.CharField(max_length=1, choices=WHICH_CHOICES, default=first)
    question_number = models.IntegerField(blank=True, validators=[MinValueValidator(0), MaxValueValidator(40)])
    mark = models.IntegerField(blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    last_date = models.DateField(default=localdate())

    class Meta:
        ordering = ['student', 'which_quiz', 'mark', 'last_date']
        verbose_name = 'quiz'
        verbose_name_plural = 'quizzes'
        constraints = [
            models.UniqueConstraint(
                    fields=('student', 'which_quiz'),
                    name='unique_quiz'
                )
        ]
    
    def get_info(self):
        true_choices = int(self.mark/(100/self.question_number))
        false_choices = int(self.question_number-true_choices)
        empty_choices = 0

        quiz_data = [true_choices, false_choices, empty_choices]
        quiz_labels = '{true} Doğru,{false} Yanlış,{empty} Boş'.format(
            true=true_choices,
            false=false_choices,
            empty=empty_choices
        ).split(',')

        return {'quiz_data': quiz_data, 'quiz_labels': quiz_labels}


    def get_title(self):
        dict_title = {'1': 'Birinci', '2': 'İkinci', '3': 'Üçüncü', '4': 'Dördüncü'}
        return dict_title[self.which_quiz]
    
    def __str__(self):
        title = "{name}, {quiz_number}. quiz notu : {quiz_mark}".format(
            name = self.student.student_name,
            quiz_number = self.which_quiz,
            quiz_mark = self.mark
        )
        
        return title