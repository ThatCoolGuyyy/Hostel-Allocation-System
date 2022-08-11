from rest_framework import viewsets
from django.shortcuts import redirect, render
from .models import Admin, Student, Hall
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from .serializers import *
from django.core import serializers

from xhtml2pdf import pisa

message = ""



# for admin messaging
def msgg1(request):
    if 'data' in request.session:
        sender_id = request.POST["sender_id"]
        sender_name = request.POST["sender_name"]
        message = request.POST["message"]
        date = request.POST["date"]
        hallid = request.POST["hallid"]
        if message != "":

            obj = Messages.objects.create(hallid=hallid, sender_id=sender_id, sender_name=sender_name, message=message, date=date)

            msg = list(Messages.objects.values_list('sender_id', 'sender_name', 'message', 'date', 'hallid'))

            obj.save()
            
            request.session['messages1'] = {"msg": msg}
          
            return redirect(adm_home)
        else:
            return render(request, 'adm/index.html', {"error": "Password dosen't match!"})
    else:
        return redirect(p405)


# for student messaging
def msgg(request):
    if 'data1' in request.session:
        sender_id = request.POST["sender_id"]
        sender_name = request.POST["sender_name"]
        message = request.POST["message"]
        date = request.POST["date"]
        hallid = request.POST["hallid"]


        if message != "":
            
            obj = Messages.objects.create(hallid=hallid, sender_id=sender_id, sender_name=sender_name, message=message, date=date)

            msg = list(Messages.objects.values_list('sender_id', 'sender_name', 'message', 'date', 'hallid'))

            obj.save()
            
            request.session['messages'] = {"msg": msg}
            return redirect(st_home)
        else:
            return render(request, 'st/index.html', {"error": "Password dosen't match!"})
    else:
        return redirect(p404)

class MessageView(viewsets.ModelViewSet):
    serializer_class = MessageSerializers
    queryset = Messages.objects.all()

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        data = {
            "lname": request.session["data1"]["lname"],
            "fname": request.session["data1"]["fname"],
            "hall_name": request.session["data1"]["hall_name"],
            "gender": request.session["data1"]["gender"],
            "matric": request.session["data1"]["matric"],
            "room_no": request.session["data1"]["r_number"],
            "appr": "Approved",
            "mail": request.session["data1"]["email"],
        }

        pdf = render_to_pdf('doc.html', data)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Information_%s.pdf" % (
            str(request.session["data1"]["matric"]))
        content = "attachment; filename=%s" % (filename)
        response['Content-Disposition'] = content
        return response

def adm_approve_st(request):
    import random
    if 'data' in request.session:
        st_matric = request.POST["st"]#getting the matric number from the session

        # Getting the number of rooms of the hall the admin is in
        hall_room_num = Hall.objects.get(
            hall_id=request.session['data']['hallID']).number_of_rooms

        rooms = []

        [rooms.append(i) for i in range(1, (hall_room_num + 1))]

        while True:
            r_num = random.choice(rooms)#infinity loop to check the check the rooms that are free and if its full, it goes to another room
            res = Student.objects.filter(room_number=r_num).count()

            if res == 4:
                pass
            else:
                break
        
        # if a room number have been gotten
        if r_num:
            # get the student data
            st_data = Student.objects.get(matric=st_matric)

            # assign the room number to the student
            st_data.room_number = "Room " + str(r_num)

            # change the student status
            st_data.approved = True
            st_data.pending = False

            # comitting chnages
            st_data.save()
            
            return redirect(adm_st)
        print("error")

    return redirect(p404)


def adm_al_st(request):
    if 'data' in request.session:
        data = Admin.objects.get(email=request.session['data']['email'])

        adm = Admin.objects.get(email=request.session['data']['email']).hallid

        h_data = Hall.objects.get(hall_id=adm).name
        h_num = Hall.objects.get(hall_id=adm).capacity
        if Student.objects.filter(hallid=adm, approved=True).exists():
            num = Student.objects.filter(hallid=adm, approved=True).count()
        else:
            num = 0

        if Student.objects.filter(pending=True).exists():
            num_pend = Student.objects.filter(pending=True, hallid=adm).count()
            std = Student.objects.filter(hallid=adm, approved=True)
        else:
            num_pend = 0

        num_room = Hall.objects.get(
            hall_id=adm).number_of_rooms

        n_per = (num/h_num) * 100
        rem_room_num = num/4
        rem_rem_room_num = num % 4
        rem_room_num_per = ((num_room - int(rem_room_num)) / num_room) * 100

        request.session['data'] = {
            "id": data.admin_id,
            "fname": data.fname,
            "lname": data.lname,
            "email": data.email,
            "num_room": num_room,
            "hallID": data.hallid,
            "hall_number": h_num,
            "rem_room_num": num_room - int(rem_room_num),
            "rem_rem_room_num": rem_rem_room_num,
            "num_per": n_per,
            "num_in_hall": num,
            "rem_room_num_per": rem_room_num_per,
            "hall_name": h_data,
            "num_pend": num_pend,
            "password": data.password,
        }
        request.session.modified = True
        return render(request, 'adm/all-student.html', {'results': std})
    return redirect(adm_login)


def adm_st(request):
    if 'data' in request.session:
        data = Admin.objects.get(email=request.session['data']['email'])

        adm = Admin.objects.get(email=request.session['data']['email']).hallid

        h_data = Hall.objects.get(hall_id=adm).name
        h_num = Hall.objects.get(hall_id=adm).capacity
        if Student.objects.filter(hallid=adm, approved=True).exists():
            num = Student.objects.filter(hallid=adm, approved=True).count()
        else:
            num = 0

        if Student.objects.filter(pending=True).exists():
            num_pend = Student.objects.filter(pending=True, hallid=adm).count()
            std = Student.objects.filter(pending=True, hallid=adm)
        else:
            num_pend = 0

        num_room = Hall.objects.get(
            hall_id=adm).number_of_rooms

        n_per = (num/h_num) * 100
        rem_room_num = num/4
        rem_rem_room_num = num % 4
        rem_room_num_per = ((num_room - int(rem_room_num)) / num_room) * 100

        request.session['data'] = {
            "id": data.admin_id,
            "fname": data.fname,
            "lname": data.lname,
            "email": data.email,
            "num_room": num_room,
            "hallID": data.hallid,
            "hall_number": h_num,
            "rem_room_num": num_room - int(rem_room_num),
            "rem_rem_room_num": rem_rem_room_num,
            "num_per": n_per,
            "num_in_hall": num,
            "rem_room_num_per": rem_room_num_per,
            "hall_name": h_data,
            "num_pend": num_pend,
            "password": data.password,
        }
        request.session.modified = True
        return render(request, 'adm/table-basic.html', {'results': std})
    return redirect(adm_login)


def home(request):
    return redirect(st_login)


def st_choose_hall(request):
    if 'data1' in request.session:

        hall = request.POST["hall"]
        reg1 = Student.objects.get(matric=request.session["data1"]["matric"])
        reg1.hallid = hall
        reg1.pending = True
        reg1.approved = False
        reg1.save()
        data = Student.objects.get(matric=request.session['data1']['matric'])

        h_data1 = Hall.objects.get(hall_id=data.hallid).name
        print(h_data1)
        request.session['data1']['hall_name'] = h_data1
        request.session['data1']['message'] = "Hall Chosen"
        request.session.modified = True
        # print(request.session['data1'])
        # message = "Hall Chosen"
        # st_hall(request, message)
        return redirect(st_hall)
    else:
        return redirect(p404)


def adm_login(request):
    return render(request, 'adm_login.html')


def st_login(request):
    return render(request, 'st_login.html')

def st_index(request):
    return render(request, '/st/index.html')


def st_home(request):
    if 'data1' in request.session:
        matric = request.session['data1']['matric']

        data = Student.objects.get(matric=matric)

        if data.hallid == 0:
            h_data = ""
        else:
            h_data = Hall.objects.get(hall_id=data.hallid).name
        request.session['data1'] = {
            "id": data.stud_id,
            "fname": data.fname,
            "lname": data.lname,
            "email": data.email,
            "gender": data.gender,
            "matric": matric,
            "hallID": data.hallid,
            "pending": data.pending,
            "approved": data.approved,
            "hall_name": h_data,
            "r_number": data.room_number,
            "password": request.session['data1']['password'],
        }

        msg = list(Messages.objects.values_list('sender_id', 'sender_name', 'message', 'date', 'hallid'))
            
        request.session['messages'] = {"msg": msg}
            
        return render(request, 'st/index.html')
    return redirect(st_login)


def st_hall(request):
    if 'data1' in request.session:
        # request.session.modified = True
        # print(request.session['data1']['hall_name'])
        if 'message' not in request.session['data1']:
            print("here1")
            return render(request, 'st/table-basic.html')
        else:
            print("here2")
            message = request.session['data1']['message']
            del request.session['data1']['message']
            request.session.modified = True

            return render(request, 'st/table-basic.html', {"message": message})

    return redirect(st_login)


def adm_home(request):
    if 'data' in request.session:
        data = Admin.objects.get(email=request.session['data']['email'])

        adm = Admin.objects.get(email=request.session['data']['email']).hallid

        h_data = Hall.objects.get(hall_id=adm).name
        h_num = Hall.objects.get(hall_id=adm).capacity
        if Student.objects.filter(hallid=adm, approved=True).exists():
            num = Student.objects.filter(hallid=adm, approved=True).count()
        else:
            num = 0

        if Student.objects.filter(pending=True).exists():
            num_pend = Student.objects.filter(pending=True, hallid=adm).count()
        else:
            num_pend = 0

        num_room = Hall.objects.get(
            hall_id=adm).number_of_rooms

        n_per = (num/h_num) * 100
        rem_room_num = num/4
        rem_rem_room_num = num % 4
        rem_room_num_per = ((num_room - int(rem_room_num)) / num_room) * 100

        request.session['data'] = {
            "id": data.admin_id,
            "fname": data.fname,
            "lname": data.lname,
            "email": data.email,
            "num_room": num_room,
            "hallID": data.hallid,
            "hall_number": h_num,
            "rem_room_num": num_room - int(rem_room_num),
            "rem_rem_room_num": rem_rem_room_num,
            "num_per": n_per,
            "num_in_hall": num,
            "rem_room_num_per": rem_room_num_per,
            "hall_name": h_data,
            "num_pend": num_pend,
            "password": data.password,
            # "hall_name": h_data,
        }
        request.session.modified = True


        msg = list(Messages.objects.values_list('sender_id', 'sender_name', 'message', 'date', 'hallid'))
            
        request.session['messages1'] = {"msg": msg}

        return render(request, 'adm/index.html')
    return redirect(adm_login)


def adm_profile(request):
    if 'data' in request.session:
        return render(request, 'adm/pages-profile.html')
    return redirect(index)


def st_profile(request):
    if 'data1' in request.session:
        return render(request, 'st/pages-profile.html')
    return redirect(st_login)


def index(request):
    return render(request, 'index.html')


def admin_index(request):
    return render(request, 'admin_index.html')


def p404(request):
    return render(request, 'st/pages-error-404.html')


def p405(request):
    return render(request, 'adm/pages-error-404.html')


def LO_student(request):
    if 'data1' in request.session:
        del request.session["data1"]
        return redirect(st_login)
    return redirect(p404)


def LO_admin(request):
    if 'data' in request.session:
        del request.session["data"]
        return redirect(adm_login)
    return redirect(p405)


def C_student(request):
    fname = request.POST["fname"]
    lname = request.POST["lname"]
    email = request.POST["email"]
    gd = request.POST["gd"]
    matric = request.POST["matric"]
    pass1 = request.POST["pass1"]
    pass2 = request.POST["pass2"]

    error = []

    if pass1 != pass2:
        error += ["Passwords don't match"]
    if Student.objects.filter(email=email).exists():
        error += ["Email not available"]
    if Student.objects.filter(matric=matric).exists():
        error += ["Matric number already assigned to a student"]

    if len(error) == 0:
        reg = Student(fname=fname, lname=lname, email=email,
                      gender=gd, matric=matric, password=pass1)
        reg.save()
        data = Student.objects.get(matric=matric)
        if Hall.objects.filter(hall_id=data.hallid).exists():
            h_data = Hall.objects.get(hall_id=data.hallid).name
        else:
            h_data = ""
        data = Student.objects.get(matric=matric)
        request.session['data1'] = {
            "id": data.stud_id,
            "fname": data.fname,
            "lname": data.lname,
            "email": data.email,
            "gender": data.gender,
            "matric": matric,
            "hall_name": h_data,
            "hallID": data.hallid,
            "pending": data.pending,
            "r_number": data.room_number,
            "approved": data.approved,
            "password": pass1,
        }
        return redirect(st_home)
    else:
        return render(request, 'index.html', {"error": error})


def C_admin(request):
    fname = request.POST["fname"]
    lname = request.POST["lname"]
    email = request.POST["email"]
    gd = request.POST["gd"]
    hallid = int(request.POST["hallid"])
    pass1 = request.POST["pass1"]
    pass2 = request.POST["pass2"]
    # hido = Hall.objects.get(hall_id=hallid)
    error = []

    if pass1 != pass2:
        error += ["Passwords don't match"]
    if Admin.objects.filter(email=email).exists():
        error += ["Email not available"]
    if Admin.objects.filter(hallid=hallid).exists():
        error += ["Hall admin already appointed to specified hall"]
    if len(error) == 0:
        password = request.POST["pass1"]
        error = ""
        reg = Admin(fname=fname, lname=lname, email=email,
                    password=password, hallid=hallid)
        reg.save()
        data = Admin.objects.get(email=email)
        h_data = Hall.objects.get(hall_id=hallid).name
        h_num = Hall.objects.get(hall_id=hallid).capacity
        num_room = Hall.objects.get(hall_id=hallid).number_of_rooms

        adm = Admin.objects.get(email=email).hallid

        if Student.objects.filter(hallid=adm, approved=True).exists():
            num = Student.objects.filter(hallid=adm, approved=True).count()
        else:
            num = 0

        if Student.objects.filter(pending=True).exists():
            num_pend = Student.objects.filter(pending=True).count()
        else:
            num_pend = 0

        n_per = (num/h_num) * 100

        rem_room_num = num/4
        rem_rem_room_num = num % 4
        rem_room_num_per = ((num_room - int(rem_room_num)) / num_room) * 100
        # print(h_)
        # nm = str(Hall.objects.get(hall_id=data.hall_id.hall_id).name)
        request.session['data'] = {
            "id": data.admin_id,
            "fname": data.fname,
            "lname": data.lname,
            "email": data.email,
            "rem_room_num": num_room - int(rem_room_num),
            "rem_rem_room_num": rem_rem_room_num,
            "rem_room_num_per": rem_room_num_per,
            "hallID": data.hallid,
            "hall_name": h_data,
            "num_room": num_room,
            "num_per": n_per,
            "num_in_hall": num,
            "num_pend": num_pend,
            "hall_number": h_num,
            "password": data.password,
            # "hall_name": h_data,
        }
        # print(nm)
        # datas = {"data": data}

        return redirect(adm_home)
    else:
        return render(request, 'admin_index.html', {"error": error})


def U_student(request):
    if 'data1' in request.session:
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        gender = request.POST["gd"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]
        ide = request.session['data1']['id']
        if pass1 == pass2:
            res = Student.objects.get(stud_id=ide)
            res.fname = fname
            res.lname = lname
            res.email = email
            res.gender = gender
            res.password = pass1
            res.save()
            data = Student.objects.get(email=email)
            # print(data.hallid)
            # h_data = Hall.objects.get(hall_id=data.hallid).name
            request.session['data1'] = {
                "id": request.session['data1']['id'],
                "fname": fname,
                "lname": lname,
                "email": email,
                # "hall_name": h_data,
                "r_number": data.room_number,
                "gender": gender,
                "matric": request.session['data1']['matric'],
                "hallID": request.session['data1']['hallID'],
                "pending": request.session['data1']['pending'],
                "approved": data.approved,
                "password": pass1,
            }

            return redirect(st_profile)
        else:
            return render(request, 'st/pages-profile.html', {"error": "Password dosen't match!"})
    else:
        return redirect(p404)


def U_admin(request):
    if 'data' in request.session:
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        adm = Admin.objects.get(email=request.session['data']['email']).hallid
        h_num = Hall.objects.get(
            hall_id=request.session['data']['hallID']).capacity
        if Student.objects.filter(hallid=adm, approved=True).exists():
            num = Student.objects.filter(hallid=adm, approved=True).count()
        else:
            num = 0

        if Student.objects.filter(pending=True).exists():
            num_pend = Student.objects.filter(pending=True).count()
        else:
            num_pend = 0

        num_room = Hall.objects.get(
            hall_id=request.session['data']['hallID']).number_of_rooms

        n_per = (num/h_num) * 100
        if pass1 == pass2:
            # print(request.session['data']['id'])
            res = Admin.objects.get(admin_id=request.session['data']['id'])
            res.fname = fname
            res.lname = lname
            res.email = email
            res.password = pass1
            res.save()
            rem_room_num = num/4
            rem_rem_room_num = num % 4
            rem_room_num_per = (
                (num_room - int(rem_room_num)) / num_room) * 100
            request.session['data'] = {
                "id": request.session['data']['id'],
                "fname": fname,
                "lname": lname,
                "email": email,
                "hall_number": h_num,
                "num_room": num_room,
                "rem_room_num_per": rem_room_num_per,
                "num_in_hall": num,
                "num_pend": num_pend,
                "rem_room_num": num_room - int(rem_room_num),
                "rem_rem_room_num": rem_rem_room_num,
                "num_per": n_per,
                "hallID": request.session['data']['hallID'],
                "password": pass1,
            }

            return redirect(adm_profile)
        else:
            return render(request, 'adm/pages-profile.html', {"error": "Password dosen't match!"})
    return redirect(p405)


def L_admin(request):
    email = request.POST["email"]
    pwd = request.POST["pwd"]

    if Admin.objects.filter(email=email, password=pwd).exists():
        adm = Admin.objects.get(email=email).hallid
        # print(Admin.objects.filter(email=email))
        h_data = Hall.objects.get(hall_id=adm).name
        h_num = Hall.objects.get(hall_id=adm).capacity
        if Student.objects.filter(hallid=adm, approved=True).exists():
            num = Student.objects.filter(hallid=adm).count()
        else:
            num = 0

        if Student.objects.filter(pending=True).exists():
            num_pend = Student.objects.filter(pending=True, hallid=adm).count()
        else:
            num_pend = 0

        num_room = Hall.objects.get(
            hall_id=adm).number_of_rooms

        n_per = (num/h_num) * 100

        data = Admin.objects.get(email=email)
        # request.session['data'] = data
        rem_room_num = num/4
        rem_rem_room_num = num % 4
        rem_room_num_per = ((num_room - int(rem_room_num)) / num_room) * 100
        request.session['data'] = {
            "id": data.admin_id,
            "fname": data.fname,
            "lname": data.lname,
            "email": data.email,
            "num_room": num_room,
            "hallID": data.hallid,
            "hall_number": h_num,
            "rem_room_num": num_room - int(rem_room_num),
            "rem_rem_room_num": rem_rem_room_num,
            "num_per": n_per,
            "num_in_hall": num,
            "rem_room_num_per": rem_room_num_per,
            "hall_name": h_data,
            "num_pend": num_pend,
            "password": data.password,
            # "hall_name": h_data,
        }
        return redirect(adm_home)
    return render(request, 'adm_login.html', {"error": "User does not exit"})


def L_student(request):
    matric = request.POST["matric"]
    pwd = request.POST["pwd"]

    if Student.objects.filter(matric=matric, password=pwd).exists():
        data = Student.objects.get(matric=matric)

        if data.hallid == 0:
            h_data = ""
        else:
            h_data = Hall.objects.get(hall_id=data.hallid).name

        request.session['data1'] = {
            "id": data.stud_id,
            "fname": data.fname,
            "lname": data.lname,
            "email": data.email,
            "gender": data.gender,
            "matric": matric,
            "hallID": data.hallid,
            "pending": data.pending,
            "r_number": data.room_number,
            "approved": data.approved,
            "hall_name": h_data,
            "password": pwd,
        }
        return redirect(st_home)
    return render(request, 'st_login.html', {"error": "User does not exit"})
