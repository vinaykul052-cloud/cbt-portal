#from django.shortcuts import  render, redirect
from django.contrib.auth.hashers import make_password, check_password
#from django.utils import timezone

# Create your views here.
#from django.shortcuts import render
from .models import Question, Student
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
       # password = request.POST.get('password')
        password = make_password(request.POST.get('password'))

        Student.objects.create(
            name=name,
            email=email,
            password=password
        )

        return render(request,'register.html', {'message': 'Registered Successfully'})
    
    return render(request,'register.html')


        #return redirect('login')
    
    #return render(request,'register.html')


#login view
def login_view(request):
   
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            #student = Student.objects.get(email=email,password=password) #kyuki password hash kr diya hai then ye line work nhi kregi
            student = Student.objects.get(email=email)
            print("User entered password:", password)
            print("Stored hashed password:", student.password) #ye debug ke liye hai, ye hashed password show krega
            #password verify -----> import check_password ke through hoga
            if check_password(password,student.password):
                request.session['student_id'] = student.id
                if student.role == "admin":
                    return redirect('admin_dashboard') #admin panel ke liye redirect krna hai
                else:
                    return redirect('dashboard')
            else:
                return render(request,'login.html', {'error':'Invalid Password'})
        except Student.DoesNotExist:
            return render(request,'login.html',{'error': 'User not found'})
    return render(request,'login.html')
                       #session create
          #  request.session['student_id'] = student.id
         #   return redirect('dashboard')
        #except Exception as e:
        #    print(e)      #debug ke liye
        #    return render(request,'login.html', {'error': 'Invalid Credentials'})
        
            
   # return render(request,'login.html') #GET request ke liye hai
    
#dashboard view
from .models import Response
def dashboard(request):
    if 'student_id' not in request.session:
        return redirect('login')
    student = Student.objects.get(id=request.session['student_id'])
     #Admin ko dashboard  mei aane se rokne ke liye
   # if student.role == 'admin':
   #     return redirect('admin_dashboard')
    responses = Response.objects.filter(student=student)
    
    score = 0
    total = 0

    for res in responses:
        if res.question.question_type == 'MCQ':
            total += 1
            if res.selected_option == res.question.correct_answer:
                score += 1

    has_attempted = responses.exists()
    return render(request, 'dashboard.html', {
        'student': student,
        'score': score,
        'total': total,
        'has_attempted': has_attempted

    })


#logout view
def logout_view(request):
    request.session.flush()  #session destroy
    return redirect('login')
#payment view 
def payment_view(request):
    if 'student_id' not in request.session:
        return redirect('login')
    student = Student.objects.get(id=request.session['student_id'])

    if request.method == 'POST':
        proof = request.FILES.get('payment_proof')

        if proof:
            student.payment_proof = proof
            student.save()

        #return render(request,'payment_pending.html')
        return redirect('dashboard')
    
    return render(request, 'payment.html')


#Exam view(questions display + save answers)
from django.shortcuts import render, redirect
from django.utils import timezone
import random

def exam_view(request):
    if 'student_id' not in request.session:
        return redirect('login')

    student = Student.objects.get(id=request.session['student_id'])

    # payment check
    if not student.payment_status:
        return render(request, 'payment_pending.html')

    # agar already exam diya hai
    if Response.objects.filter(student=student).exists():
        return redirect('result')

    # ================================
    # GET REQUEST
    # ================================
    if request.method == 'GET':
        questions = list(Question.objects.all())
        random.shuffle(questions)
        questions = questions[:5]

        # session mei store karo
        request.session['questions'] = [q.id for q in questions]

        # start time
        request.session['start_time'] = str(timezone.now())

        return render(request, 'exam.html', {'questions': questions})

    # ================================
    # POST REQUEST
    # ================================
    else:
        question_ids = request.session.get('questions', [])
        questions = Question.objects.filter(id__in=question_ids)

        print("POST DATA:", request.POST)

        for question in questions:
            if question.question_type == 'MCQ':
                selected = request.POST.get(str(question.id))
                print("Saving MCQ:", question.id, selected)

                Response.objects.create(
                    student=student,
                    question=question,
                    selected_option=selected
                )

            else:
                text_answer = request.POST.get(f"text_{question.id}")
                print("Saving SUBJECTIVE:", question.id, text_answer)

                Response.objects.create(
                    student=student,
                    question=question,
                    answer_text=text_answer
                )

        return redirect('result')


#Basic Result system (AUto MCQ check)

def result_view(request):
    if 'student_id' not in request.session:
        return redirect('login')
    student = Student.objects.get(id=request.session['student_id'])
    
    #agar publish nahi hua

    if not student.result_published:
        return render(request, 'result.html', { 
            'not_published': True           
        })
    responses = Response.objects.filter(student=student)

    mcq_score = 0
    subjective_score = 0
    total_mcq = 0

    for res in responses:
        #MCQ
        if res.question.question_type == 'MCQ':
            total_mcq +=1
            if res.selected_option == res.question.correct_answer:
                mcq_score +=1

                #subjective
        else:
            if res.marks:
                subjective_score += res.marks
    
    total_score = mcq_score + subjective_score
    return render(request,'result.html',{
        'mcq_score': mcq_score,
        'subjective_score': subjective_score,
        'total_score': total_score,
        'total_mcq': total_mcq
    })

def admin_dashboard(request):
    if 'student_id' not in request.session:
        return redirect('login')
    student = Student.objects.get(id=request.session['student_id'])

    if student.role != 'admin':
        return redirect('login')
    #loop avoid krega
    students = Student.objects.all()
    return render(request,'admin_dashboard.html', { 'students': students })

def approve_payment(request, id):
    student = Student.objects.get(id=id)
    student.payment_status = True
    student.payment_date = timezone.now()
    student.save()
    return redirect('admin_dashboard')

def check_response(request, student_id):
    student = Student.objects.get(id=student_id)
    responses = Response.objects.filter(student=student)
    if request.method == 'POST':
        for res in responses:
            marks = request.POST.get(f"marks_{res.id}")
            if marks:
                res.marks = int(marks)
                res.save()
        return redirect('admin_dashboard')
    return render(request,'check_response.html',{'student': student, 'responses': responses})


def publish_result(request, id):
    student = Student.objects.get(id=id)
    student.result_published = True
    student.save()
    return redirect('admin_dashboard')