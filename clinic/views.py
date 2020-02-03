import django_filters
from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.shortcuts import redirect, render

from clinic.models import Appointment
from clinic.models import Doctor
from clinic.models import Patient
from clinic.models import Receptionist
from clinic.models import Record
from clinic.models import User


def appointment_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('home')
    else:
        form = AppointmentForm()
    return render(request, 'receptionists/appointment.html', {'form1': form})


def search(request):
    patient_list = Patient.objects.all()
    patient_filter = PatientFilter(request.GET, queryset=patient_list)
    return render(request,'patients/search.html', {'filter': patient_filter})


class PatientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Patient
        fields = ['name','id']


def add_patient_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PatientForm()
    return render(request, 'patients/createpat.html', {'form': form})


def add_record_view(request,pk):
        if request.method == 'POST':
            f = RecordForm(request.POST)
            if f.is_valid():
                pat=Patient.objects.get(id=pk)
                f.fields['patient']= pat
                f.save()
                return redirect('home')
        else:
            f = RecordForm()
        return render(request, 'patients/createre.html', {'form2': f})


def list_appointment_view(request):
    current_user = request.user
    doctor=current_user.doc
    app_set = doctor.appointments.all().order_by('time')
    return render(request,'doctors/appointments.html',{"appointments":app_set})


def details(request,pk):
    pat=Patient.objects.get(id=pk)
    rec=pat.records.all()
    return render(request, 'patients/details.html', {'rec': rec ,'pat':pat})


def recup(request):
    if request.method == 'POST':
        orm = SignUpForm(request.POST)
        if orm.is_valid():
            orm.save()
            username = orm.cleaned_data.get('username')
            raw_password = orm.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            rec=Receptionist.objects.create(user=user)
            temp =User.objects.get(username=username)
            temp.is_receptionist = True
            login(request, user)
            return redirect('home')
    else:
        orm = SignUpForm()
    return render(request, 'receptionists/createrec.html', {'form3': orm})


def docup(request):
    if request.method == 'POST':
        rm = SignUpForm(request.POST)
        if rm.is_valid():
            rm.save()
            username = rm.cleaned_data.get('username')
            raw_password = rm.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            doc = Doctor.objects.create(user=user)
            temp = User.objects.get(username=username)
            temp.is_doctor = True
            login(request, user)
            return redirect('home')
    else:
        rm = SignUpForm()
    return render(request, 'doctors/createdoc.html', {'form4': rm})


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )

'''
class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class DoctorSignUpView(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'doctor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('TODOO!!!!')
'''


def rechome(request):
    if request.user.is_authenticated:
        if request.session['is_doc'] is True:
            return redirect('dochome')
        else:
            return render(request, 'receptionists/rechome.html')
    else:
        return redirect('home')


def home(request):
    if request.user.is_authenticated:

        t1=Doctor.objects.all()
        for x in t1:
            if x.user.id is request.user.id:
                request.session['is_doc'] = True

        t2=Receptionist.objects.all()
        for y in t2:
            if y.user.id is request.user.id:
                request.session['is_doc'] = False

        if request.session['is_doc'] is True:
            return redirect('dochome')
        else:
            return redirect('rechome')

    return render(request, 'home.html')


def dochome(request):
    if request.user.is_authenticated:
        if request.session['is_doc'] is False:
            return redirect('rechome')
        else:
            return render(request, 'doctors/dochome.html')
    else:
        return redirect('home')



class RecordForm(forms.ModelForm):

    class Meta:
        model = Record
        fields =['patient','created_by','title','text']



class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields =['name','sex']



class AppointmentForm(ModelForm):

    class Meta:
        model = Appointment
        fields =['time','patient','doctor']



'''
class DoctorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_doctor = True
        user.save()
        doctor = Doctor.objects.create(user=user)
        return user


class ReceptionistSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_receptionist = True
        user.save()
        receptionist = Receptionist.objects.create(user=user)
        return user
'''

