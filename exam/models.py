

# Create your models here.
from django.db import models
class Student(models.Model):
    name =models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    role = models.CharField(max_length=10,default='student')    #ye real admin and student jaisa wesite bnayega
                       #payment field yaha add kr lege
    payment_status = models.BooleanField(default=False)    
    payment_date = models.DateTimeField(null=True, blank=True)
    
    payment_proof = models.ImageField(upload_to='payments/',null=True, blank=True) # student payment ka screenshot upload krega jisse payment proff hoga

    result_published = models.BooleanField(default=False)  #ye redult ko published krega

    def __str__(self):
        return f"{self.name} ({self.role})"

class Question(models.Model):
    QUESTION_TYPES = (
        ('MCQ', 'MCQ'),
        ('SUBJECTIVE', 'Subjective'),
    )

    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices= QUESTION_TYPES)
      
          #MCQ options

    option1 = models.CharField(max_length=200,blank=True, null=True)
    option2 = models.CharField(max_length=200,blank=True, null=True)
    option3 = models.CharField(max_length=200,blank=True, null=True)
    option4 = models.CharField(max_length=200,blank=True, null=True)
   # option5 = models.CharField(max_length=200,blank= True,null=True)

    correct_answer = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return self.question_text

#class response
class Response(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question= models.ForeignKey(Question, on_delete=models.CASCADE)

         #answer field
    selected_option = models.CharField(max_length=10,blank=True, null=True) #ye MCQ ke liye hai
    answer_text = models.TextField(null=True,blank=True) #ab ye subjective ke liye ho gyi hai
    marks = models.IntegerField(null=True,blank=True)

    #subjective_answer = models.TextField(blank=True, null=True) #ye subjective ke liye hai

    def __str__(self):
        return f"{self.student.name} - {self.question.id}"
    