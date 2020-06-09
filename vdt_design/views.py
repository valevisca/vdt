from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
# We import the User object from the following library
from django.contrib.auth.models import User
# We import now the login method 
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
# Import the FileStorage object to manage filesize
from django.core.files.storage import FileSystemStorage
from .forms import DesignForm, PidForm
from .models import Design, Pid
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Enabling inpor-export
from django.http import HttpResponse
from .resources import PidResource
# Adding now the pre and post processing Pandas and NumPy capabilities
import pandas as pd
import numpy as np
from xlrd import XLRDError
import os


# Create your views here.

def home(request):
    return render(request, 'vdt_design/home.html')


def signupuser(request):
    """
    NOTE: every time someone write something on a URL and then
    press <ENTER>, this is coming to the web server as a 'GET'
    request. A 'POST' request can only come through a <form>.
    We can use this to guide the action of this function.
    """
    if request.method == 'GET':
        # if the method is 'GET', we then create a new user
        return render(request, 'vdt_design/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], \
                            password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentdesigns')
            except IntegrityError:
                return render(request, 'vdt_design/signupuser.html', {
                            'form': UserCreationForm(),
                            'error':'That username has already been taken. Please choose a new one'})

        else:
            # Tell the user the passwords didn't match
            return render(request, 'vdt_design/signupuser.html', {
                            'form': UserCreationForm(),
                            'error':'Passwords did not match'})


# '@login_required' tells Django that only users who have looged in can run the next
# function
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            success_message = 'Your password was successfully updated!'
            messages.success(request, success_message)
            return render(request, 'vdt_design/change_password.html', {
                    'form': form,
                    'success_message': success_message,
                    })
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'vdt_design/change_password.html', {
                    'form': form,
                    'success_message': None,
                    'error_message': 'Please correct the error below.',
                    })
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'vdt_design/change_password.html', {
                    'form': form,
                    'success_message': None,
                    })


def loginuser(request):
    if request.method == 'GET':
        # if the method is 'GET', we then crepresent the login user
        # screen
        return render(request, 'vdt_design/loginuser.html', {
                                'form': AuthenticationForm()})
    else:
        # SE-NOTE: If the request is a 'POST', we then collect the user data,
        # check them against the stored password and authenticate the user.
        # We need another function, 'authenticate', that we have to import
        # from 'django.contrib.auth'
        # First step is to create a user, getting its username and password
        # 'authenticate' check username and password and if the user is not 
        # found or the authentication data are wrong, it reports 'none'.
        # Otherwise we can use the user to login.
        user = authenticate(request, username=request.POST['username'], \
                                    password=request.POST['password'])
        
        if user is None:
            # User not found or wrong credentials. We send him again to the 
            # authentication page, passing an error message into the
            # dictionary
            return render(request, 'vdt_design/loginuser.html', {
                                'form': AuthenticationForm(),
                                'error': 'Incorrect username or password'})
        else:
            # User is found and we can use 'user' for the login and we then
            # redirect user to the current designs web page.
            login(request, user)
            return redirect('currentdesigns')



# '@login_required' tells Django that only users who have looged in can run the next
# function
@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def upload(request):
    """
    WARNING: this method is currently NOT USED...it is a placeholder from a simpler Django project.
    Please refer to 'designupload()'...
    """
    if request.method == 'POST':
        uploadedfile = request.FILES['document']
        # We create an object instance
        fs = FileSystemStorage()
        # and then save it using the 'save' method. Save returns the filename that can be used
        filename = fs.save(uploadedfile.name,  uploadedfile)
        # The link to the file can be generated with the method 'url'
        fileurl = fs.url(filename)
        # SE-NOTE: we could have used 'uploadedfile.name', but this is the original file's name. If the
        # file is already in the media folder, Django automatically append some random characters and
        # this also mean that the only way to be sure to point to the right file is to refer to the file
        # using 'filename'
        return render(request, 'vdt_design/upload.html', {'fileurl':fileurl})
    #else:
    #    return render(request, 'vdt_design/upload.html')


@login_required
def currentdesigns(request):
    """
    Import the Designs from the Db, using the Todo object (see import section)
    NOTE: todos = Todo.objects.all() gets all the todos for every user. We need
    to be more specific than this.
    """
    # First we retrieve all the Design.objects for the current user
    designs = Design.objects.filter(user=request.user)
    return render(request, 'vdt_design/currentdesigns.html', {'designs':designs})


@login_required
def designupload(request):
    if request.method == 'GET':
        # The request is a 'GET', we instantiate an empty form and pass it to the designupload
        return render(request, 'vdt_design/designupload.html', {
                                'form': DesignForm()
        })
    else:
        try:
            # If request is 'POST', we instantiate a form retrieving the data from the POST
            form = DesignForm(request.POST, request.FILES)
            print("Doing the POST")
            # Then we check if the form is valid and def save(self, *args, **kwargs):
            if form.is_valid():
                print("Form is valid")
                # We then create a new variable, called newtodo, where we temporarly store
                # the form. NOTE 'commit=False', which means we do not store the form to 
                # the Db yet, as we have to assign the todo to a specific user.
                newdesign = form.save(commit=False)
                print(newdesign, request.user)
                newdesign.user = request.user
                newdesign.save()
                return redirect('currentdesigns')
        except ValueError:
            return render(request, 'vdt_design/designupload.html', {
                            'form': DesignForm(),
                            'error': 'Bad Input Data. Please try again.'})   


@login_required
def viewdesign(request, design_pk):
    # To get the design details we use the 'get_object_or_404' method we imported to retrieve 
    # the object from the 'Design' model.
    # 'design' the instance wiht 'pk' (primary key in Db terminology) equal to the
    # 'design_id'
    design = get_object_or_404(Design, pk=design_pk, user=request.user)
    #FILE_PATH = os.path.join(BASE_DIR, design.inputfile)
    # SE-NOTE: The next step is to present the design details or to retrieve the modifications. 
    # To differentiate between the two, as usual, we use the 'GET' method (present the Design details)
    # or the 'POST' method, to collect any modifications
    if request.method == 'GET':
        # We pass the Design object using the DesignForm and then pass both to the template via 
        # render as a dictionary
        form = DesignForm(instance=design)
        oldfilepath = design.inputfile.path
        print("Old design file is: ", oldfilepath)
        try:
            df_sites = pd.read_excel(design.inputfile, 'sites', index_col=None, na_values=['NA'])
            df_nodes = pd.read_excel(design.inputfile, 'nodes', index_col=None, na_values=['NA'])
            return render(request, 'vdt_design/viewdesign.html', {
                        'design':design, 
                        'form':form, 
                        'df_sites':df_sites.to_html,
                        'df_nodes':df_nodes.to_html,
                        })
        except XLRDError:
            return render(request, 'vdt_design/viewdesign.html', {
                        'design':design, 
                        'form':form,
                        'error': 'No sheet named <\'sites\'> or <\'nodes\'>',
                        }) 
    else:
        try:
            # We get the form from the html page
            # SE_NOTE: WARNING!!!! It is important to include the request.FILES, to collect the files
            # objects from the form.
            # THE <FOMR> IN THE TEMPLATE MUST have enctype="multipart/form-data" specified!!!
            form = DesignForm(request.POST, request.FILES, instance=design)
            # And simply def save(self, *args, **kwargs):
            if form.is_valid():
                # We then create a new variable, called newtodo, where we temporarly store
                # the form. NOTE 'commit=False', which means we do not store the form to 
                # the Db yet, as we have to assign the todo to a specific user
                
                #print("Form data: ", form.data)
                if 'inputfile' in form.changed_data:
                    print("Old file path is: ", design.inputfile.path)
                    print('Input File Has changed')
                form.save()
                return redirect('currentdesigns')
        except ValueError:
            return render(request, 'vdt_design/viewdesign.html', {
                            'design': design,
                            'form': form,
                            'error': 'Bad info'})

    return render(request, 'vdt_design/viewdesign.html')



@login_required
def analysedesign(request, design_pk):
    # To get the design details we use the 'get_object_or_404' method we imported to retrieve 
    # the object from the 'Design' model.
    # 'design' the instance wiht 'pk' (primary key in Db terminology) equal to the
    # 'design_id'
    design = get_object_or_404(Design, pk=design_pk, user=request.user)
    # SE-NOTE: The next step is to present the design details or to retrieve the modifications. 
    # To differentiate between the two, as usual, we use the 'GET' method (present the Design details)
    # or the 'POST' method, to collect any modifications
    if request.method == 'POST':
        # We pass the Design object using the DesignForm and then pass both to the template via 
        # render as a dictionary
        form = DesignForm(instance=design)
        try:
            df_sites = pd.read_excel(design.inputfile, 'sites', index_col=None, na_values=['NA'])
            df_nodes = pd.read_excel(design.inputfile, 'nodes', index_col=None, na_values=['NA'])
            return render(request, 'vdt_design/analysedesign.html', {
                        'design':design, 
                        'form':form, 
                        'df_sites':df_sites.to_html,
                        'df_nodes':df_nodes.to_html,
                        })
            
        except XLRDError:
            return render(request, 'vdt_design/analysedesign.html', {
                        'design':design, 
                        'form':form,
                        'error': 'No sheet named <\'sites\'> or <\'nodes\'>',
                        })  



@login_required
def deletedesign(request, design_pk):
    design = get_object_or_404(Design, pk=design_pk, user=request.user)
    # This has to be triggered by a 'POST' request ONLY!
    if request.method == 'POST':
        design.delete()
        return redirect('currentdesigns')


@login_required
def currentpids(request):
    """
    Import the pids from the Db, using the Pid object (see import section), filtering by user.
    """
    # First we retrieve all the Design.objects for the current user
    pids = Pid.objects.filter(user=request.user)
    return render(request, 'vdt_design/currentpids.html', {'pids':pids})


@login_required
def pidsupload(request):
    """
    This method load a file to memory and pass it to pandas to build a DataFrame (DF) representing the
    excel worksheet.
    We then scan through the DF to create the PIDs instances into the Db.
    We have to check if the PID exists. If it exists we overwrite the data. If not we create the data.
    In the first implementation we load the entire file to memory which should be fine, as the excel file
    containing the PIDs is supposed to be small.
    """
    if request.method == 'GET':
        # The request is a 'GET', we instantiate an empty form and pass it to the designupload
        return render(request, 'vdt_design/pidsupload.html')
    else:
        df_pids = pd.read_excel(request.FILES['document'], 'pids', index_col=None, na_values=['NA'])
        for index, row in df_pids.iterrows():
            pid_instance = Pid(
                sname = row['sym_name'],
                pidtype = row['pidtype'],
                name = row['name'],
                description = row['description'],
                cogs = round(row['cogs'],2),
                gpl = round(row['gpl'],2),
                discount = round(row['discount'],2),
                netprice = round(row['netprice'],2),
                power_typ = row['power_typ'],
                power_max = row['power_max'],
                mtbf = row['mtbf'],
                user = request.user
            )           
            pid_instance.save()
        return redirect('currentpids')

@login_required
def viewpid(request, sname):
    pid = get_object_or_404(Pid, sname=sname, user=request.user)
    if request.method == 'POST':
        form = PidForm(request.POST, instance=pid)
        if form.is_valid():
            form.save()
            return redirect('currentpids')
        else:
            return render(request, 'vdt_design/viewpid.html', {'form':form})
    else:
        form = PidForm(instance=pid)
        return render(request, 'vdt_design/viewpid.html', {'form':form, 'pid':pid})



@login_required
def createpid(request):
    """
    This method create a new PID object and stores it in the database using Pid model and PidForm.
    I am using 'sname' as primary key. I need to implement a way to generate a unique key in case the
    one submitted is already in use.
    I could also implement a search pid function.
    For now I am simply capturring the error and 
    """
    if request.method == 'GET':
        # The request is a 'GET', we instantiate an empty form and pass it to the designupload
        return render(request, 'vdt_design/createpid.html', {
                                'form': PidForm()
        })
    else:
        try:
            # If request is 'POST', we instantiate a form retrieving the data from the POST
            form = PidForm(request.POST)
            # Then we check if the form is valid and def save(self, *args, **kwargs):
            if form.is_valid():
                # We then create a new variable, called newtodo, where we temporarly store
                # the form. NOTE 'commit=False', which means we do not store the form to 
                # the Db yet, as we have to assign the todo to a specific user.
                newpid = form.save(commit=False)
                newpid.user = request.user
                newpid.save()
                return redirect('currentpids')
            else:
                return render(request, 'vdt_design/createpid.html', {
                            'form': PidForm(),
                            'error': form.errors})
        except ValueError:
            return render(request, 'vdt_design/createpid.html', {
                            'form': PidForm(),
                            'error': 'Bad Input Data. Please try again.'})   


@login_required
def deletepid(request, sname):
    pid = get_object_or_404(Pid, sname=sname, user=request.user)
    # This has to be triggered by a 'POST' request ONLY!
    if request.method == 'POST':
        pid.delete()
        return redirect('currentpids')


@login_required
def deleteallpids(request):
    """
    Import all the pids from the Db, using the Pid object (see import section), filtering by user.
    Then delete them.
    """
    # First we retrieve all the Design.objects for the current user
    pids = Pid.objects.filter(user=request.user)
    for pid in pids:
        pid.delete()

    return redirect('currentpids')


@login_required
def exportallpids(request):
    pid_resource = PidResource()
    dataset = pid_resource.export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="pid_details.xlsx"'
    return response





