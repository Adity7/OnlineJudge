from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from problem.models import Problem, Submission, Coder, TestCase
from problem.forms import UserForm, ProblemForm, SubmissionForm



def index(request):
    return render(request, "problem/index.html")


def register_user(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            # save the user to the db
            u = user_form.save()
            u.set_password(u.password)
            u.save()

            coder = Coder(user = u)
            coder.link = "/problem/users/%s" % (u.username)
            coder.score = 0
            # calculation of rank in the beginning
            coder.rank = -1
            for k in Coder.objects.all():
                coder.rank = max(coder.rank, k.rank)
            coder.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, "problem/register.html", {"user_form": user_form, "registered": registered})


def loguserin(request):
    # if form has been filled and sent by the user
    if request.method == 'POST':
        # get the username and password
        username = request.POST.get('username')
        password = request.POST.get('password')
        # authenticate the user using django's in built authenticate function
        user = authenticate(username=username, password=password)
        if user: # if the user exists log her in and redirect back to home page
            login(request, user)
            return HttpResponseRedirect('/problem/')
        else: # otherwise redirect to a page showing an error
            print("Invalid login details: {}, {}".format(username, password))
            return HttpResponse("Invalid Login Details")
    else:
        return render(request, "problem/login.html", {})


def loguserout(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect("/problem/")


def add_problem(request):
    # if user is not logged in, throw him to a sign-in page
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/problem/login/")
    else:
        if request.method == 'POST':
            problem_form = ProblemForm(request.POST, request.FILES)
            if problem_form.is_valid():
                # save a new problem
                problem = problem_form.save()
                problem.save()
                return redirect("/problem/")
            else:
                problem_form = ProblemForm()
                return render(request, "problem/addproblem.html", {"problem_form": problem_form})

def view_problem(request, pid):
    problem = get_object_or_404(Problem, code = pid)
    payload = {"problem":problem}
    return render(request, "problem/problem.html", payload)

def all_problems(request):
    problems = Problem.objects.all()
    return render(request, "problem/all.html", {"problems":problems})

def submit(request, pid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/problem/login/')
    else:
        if request.method == 'POST':
            sub_form = SubmissionForm(request.POST)
            if sub_form.is_valid():
                sub = sub_form.save()
                sub.problem = Problem.objects.get(code = pid)
                print(sub.problem.code)
                sub.submitter = Coder.objects.get(user = request.user)
                print(sub.submitter)
                sub.save()
                return HttpResponseRedirect('/problem/submission/{}'.format(sub.id))
        else:
            sub_form = SubmissionForm()
            payload = {"sub_form":sub_form, "pid":pid}
            return render(request, "problem/submit.html", payload)

def view_submission(request, submission_id):
    required_sub = get_object_or_404(Submission, id = int(submission_id))
    if not required_sub.private or (required_sub.private and required_sub.submitter.user.username == request.user.username):
        return render(request, "problem/submission.html", {"submission": required_sub})
    else:
        return HttpResponseRedirect('/problem/')
