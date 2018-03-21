from django.shortcuts import render
from django.db.models import Count, Min, Sum, Avg, Max
from datetime import timedelta

# Create your views here.

from .models import Project, Phase, Iteration, ActivityTime, DefectData, Developer, Manager, Metrics, ChangeLog

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

#Admin-log in
def userlogin(request):
    username = request.POST.get('Account')
    password = request.POST.get('Password')
    context = {'account':username, 'password':password}
    user = authenticate(username = username, password = password)
    if user is not None:
        if user.is_active:
            login(request, user)
            if request.user.groups.filter(name="Manager").exists():
                return HttpResponseRedirect("/pdt/manager_menu")
            elif request.user.groups.filter(name="Developer").exists():
                return HttpResponseRedirect("/pdt/developer_menu")
        else:
            return render(request, 'pdt/manager_menu.html', {})
    else: 
        return render(request, 'pdt/login.html', context)            

#Admin-log out
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/pdt")

#User_menu
def developer_menu(request):
    if request.user.is_authenticated():
        if request.user.groups.filter(name="Developer").exists():
            d = request.user.developer
            project_list = d.projects.values()
            name = request.user.username
            ID = request.user.pk
            context = {'project': project_list,'name':name,'ID':ID}
            return render(request, 'pdt/developer_menu.html', context)
        else:
            return render(request, 'pdt/login.html', {})
    else:
        return render(request, 'pdt/login.html', {})

#User_menu
def manager_menu(request):
    if request.user.is_authenticated():
        if request.user.groups.filter(name="Manager").exists():
            project_list = Project.objects.all()
            name = request.user.username
            ID = request.user.pk
            context = {'project': project_list,'name':name,'ID':ID}
            return render(request, 'pdt/manager_menu.html', context)
        else:
            return render(request, 'pdt/login.html', {})
    else:
        return render(request, 'pdt/login.html', {})



#Developer-get the time used for this iteration, developer
def get_activity_time(pid, did, type):
    p = Project.objects.get(project_id = pid)
    it = p.current_ite
    a_time = ActivityTime.objects.filter(iteration = it, developer = did, name = type)
    a = a_time[0]
    return a.get_time()

#Developer-update the time used for this activity, iteration, developer
def updateTime(request):
    aid = request.POST.get("aid", False)
    d = request.user.developer
    time = request.POST['time_value']
    a = ActivityTime.objects.get(pk = aid)
    a.update_time(time)
    return HttpResponse(time)

#Developer-development-timer
def development(request, pid):
    if request.user.is_authenticated():
        if request.user.groups.filter(name="Developer").exists():
            p = Project.objects.get(project_id = pid)
            d = request.user.developer
            new_activity = ActivityTime(iteration = p.current_ite, developer = d, name = 'Development', time_used = 0, starttime = timezone.now())
            new_activity.save()
            time_used = ActivityTime.objects.filter(iteration = p.current_ite, developer = d, name = 'Development').aggregate(Sum('time_used'))).values()
            context = {'name': request.user.username, 'ID': request.user.pk, 'time_used': time_used[0], 'project': p, 'aid': new_activity.pk}
            return render(request, 'pdt/development.html', context)
        else:
            return render(request, 'pdt/login.html', {})
    else:
        return render(request, 'pdt/login.html', {})

#Developer-defect removal-request information for defect removal
def new_defect_removal(request, pid):
    if request.user.is_authenticated():
        if request.user.groups.filter(name="Developer").exists():
            p = Project.objects.get(project_id = pid)
            cur_it = p.current_ite
            d = request.user.developer
            new_activity = ActivityTime(iteration = p.current_ite, developer = d, name = 'Defect Removal', time_used = 0, starttime = timezone.now())
            new_activity.save()
            time_used = ActivityTime.objects.filter(iteration = p.current_ite, developer = d, name = 'Defect Removal').aggregate(Sum('time_used'))).values()
            dict = get_before_information(pid)
            possible_ph_list = list(dict.keys())
            it_num_list = list(dict.values())
            context = {'project': p, 'name': request.user.username, 'ID': request.user.pk, 'time_used': time_used[0], 'itnum_list': it_num_list, 'new_ph_list': possible_ph_list,'aid': new_activity.pk, 'phase': cur_it.phase.get_phase_id_display(), 'phase_id': cur_it.phase.phase_id, 'iteration': cur_it.iteration_id}
            return render(request, 'pdt/defect_removal.html', context)
        else:
            return render(request, 'pdt/login.html', {})
    else:
        return render(request, 'pdt/login.html', {})

#Developer-defect removal-store new defect removal information
def defect_removal(request):
    pid = request.POST.get("pid")
    d_type = request.POST.get("type")
    d_description = request.POST.get("description")
    d_inject_ph = request.POST.get("inject_phase")
    d_inject_it = request.POST.get("inject_iteration")
    d_remove_ph = request.POST.get("remove_phase")
    d_remove_it = request.POST.get("remove_iteration")
    d = request.user.developer
    inject_ph = Phase.objects.filter(project_id = pid, phase_id = d_inject_ph)
    inject_it = Iteration.objects.filter(phase = inject_ph[0], iteration_id = d_inject_it)
    remove_ph = Phase.objects.filter(project_id = pid, phase_id = d_remove_ph)
    remove_it = Iteration.objects.filter(phase = remove_ph[0], iteration_id = d_remove_it)
    dd = DefectData(data_type = d_type, inject_iteration = inject_it[0], remove_iteration = remove_it[0], description = d_description, developer = d)
    dd.save()
    return HttpResponse("Success")

def cancel_defect_removal(request):
    aid = request.POST.get("aid")
    ActivityTime.objects.get(pk = aid).delete()


def update_and_create_log(request):
    aid = request.POST.get("aid")
    updateTimeUsed = request.POST.get("= =")
    a = ActivityTime.objects.get(pk = aid)
    l = ChangeLog(activity = a, occurTime = timezone.now(), originalTimeUsed = a.time_used, updateTimeUsed = updateTimeUsed)
    l.save()
    a.time_used = updateTimeUsed
    a.save()
    return HttpResponse("Change successfully!")

#Get a dictionary [phase -> iteration number] for phases before and including current phase
def get_before_information(pid):
    p = Project.objects.get(project_id = pid)
    cur_it = p.current_ite
    cur_ph = cur_it.phase
    possible_ph_list = Phase.objects.filter(project = p, phase_id__lte = cur_ph.phase_id)
    before_dict = {}
    for ph in possible_ph_list:
        if ph != cur_ph:
            it_list = get_phase_iteration(ph)
            before_dict[ph.get_phase_id_display()] = len(it_list)
        else:
            before_dict[ph.get_phase_id_display()] = len(Iteration.objects.filter(phase = ph, iteration_id__lte = cur_it.iteration_id).values())
    return before_dict

#Developer-defect data list-display defect data list
def defect_data_list(request, pid):
    if request.user.is_authenticated():
        if request.user.groups.filter(name="Developer").exists():
            p = Project.objects.get(project_id = pid)
            d = request.user.developer
            iteration_list = get_project_iteration_list(pid)
            defect_list = DefectData.objects.filter(remove_iteration = iteration_list, developer = d )
            new_activity = ActivityTime(iteration = p.current_ite, developer = d, name = 'Management', time_used = 0, starttime = timezone.now())
            new_activity.save();
            time_used = ActivityTime.objects.filter(iteration = p.current_ite, developer = d, name = 'Management').aggregate(Sum('time_used'))).values()
            development_list = ActivityTime.objects.filter(iteration = p.current_ite, developer = d, name = 'Development')
            management_list = ActivityTime.objects.filter(iteration = p.current_ite, developer = d, name = 'Management').exclude(pk = aid)
            context = {'pid': pid, 'name': request.user.username, 'ID': request.user.pk, 'time_used': time_used[0], 'defect_list': defect_list, 'time_used': time}
            return render(request, 'pdt/defect_data_list.html', context)
        else:
            return render(request, 'pdt/login.html', {})
    else:
        return render(request, 'pdt/login.html', {})

#Manager-classify iteration
def classify_iteration(pid):
    it_list = [get_before_iteration(pid), get_current_iteration(pid), get_after_iteration(pid)]
    return it_list

#Manager-get iteration before current iteration
def get_before_iteration(pid):
    current_p = Project.objects.get(project_id = pid)
    current_it = current_p.current_ite
    before_ph_list = Phase.objects.filter(project = current_p).filter(phase_id__lt = current_it.phase.phase_id)
    before_it_list = Iteration.objects.filter(phase = before_ph_list)
    before_it_list = list(before_it_list) + list(Iteration.objects.filter(phase = current_it.phase).filter(iteration_id__lt = current_it.iteration_id))
    return before_it_list

#Manager-get iteration current iteration
def get_current_iteration(pid):
    current_p = Project.objects.get(project_id = pid)
    return [current_p.current_ite]

#Manager-get iteration after current iteration
def get_after_iteration(pid):
    current_p = Project.objects.get(project_id = pid)
    current_it = current_p.current_ite
    after_ph_list = Phase.objects.filter(project = current_p).filter(phase_id__gt = current_it.phase.phase_id)
    after_it_list = Iteration.objects.filter(phase = after_ph_list)
    after_it_list = list(Iteration.objects.filter(phase = current_it.phase).filter(iteration_id__gt = current_it.iteration_id)) + list(after_it_list)
    return after_it_list

#Manager-Management-return iteration list information for project management display
def manage_project(request, pid):
    it_list = classify_iteration(pid)
    context = {'name': request.user.username, 'ID': request.user.pk, 'project': get_project(pid),'before_it_list': it_list[0], 'current_it_list': it_list[1], 'after_it_list': it_list[2], 'developer_list': get_project_developer(pid), 'time': get_project_time(pid), 'code_size':get_project_code_size(pid)}
    return render(request, 'pdt/manage_project.html', context)

#get project's used time
def get_project_time(pid):
    p_it_list = get_project_iteration_list(pid)
    p_time = ActivityTime.objects.filter(iteration = p_it_list).aggregate(Sum('time_used')).values()
    return p_time[0]

#get project's code size
def get_project_code_size(pid):
    p_it_list = get_project_iteration_list(pid)
    p_code_size = 0
    for it in p_it_list:
        p_code_size += it.code_size
    return p_code_size

#get project's developers
def get_project_developer(pid):
    p = Project.objects.get(project_id = pid)
    d_list = Developer.objects.filter(projects = p)
    return d_list

#get phase's developers
def get_phase_iteration(ph):
    it_list = Iteration.objects.filter(phase = ph)
    return it_list

def get_project(pid):
    p = Project.objects.get(project_id = pid)
    return p

def get_project_phase_list(pid):
    p = Project.objects.get(project_id = pid)
    ph_list = Phase.objects.filter(project = p)
    return ph_list

def get_project_iteration_list(pid):
    ph_list = get_project_phase_list(pid)
    it_list = Iteration.objects.filter(phase = ph_list)
    return it_list

def get_defect_data_list(pid):
    return 0


def defect_data_info(request, did):
    if request.user.is_authenticated():
        if request.user.groups.filter(name="Developer").exists():
            name = request.user.username
            ID = request.user.pk
            defect = DefectData.objects.get(pk = did)
            i = defect.inject_iteration
            pid = Phase.objects.get(iteration = i).project_id
            p = Project.objects.get(project_id = Phase.objects.get(iteration = i).project_id)
            time_used = ActivityTime.objects.get(iteration = p.current_ite, name = "Management", developer = defect.developer).time_used
            context = {'name':name,'ID':ID, 'defect': defect, 'time_used': time_used, 'pid': pid}
            return render(request, 'pdt/defect_info.html', context)
        else:
            return render(request, 'pdt/login.html', {}) 
    else:
        return render(request, 'pdt/login.html', {})

def defect_data_update(request):
    if request.user.is_authenticated():
        if request.user.groups.filter(name="Developer").exists():
            did=request.POST.get('did')
            defect_type=request.POST.get('type')
            description=request.POST.get('description')
            defect = DefectData.objects.get(pk = did)
            defect.data_type = defect_type
            defect.description = description
            defect.save()
            return HttpResponse("Update Successfully")
        else:
            return HttpResponse("Permission Denied")
    else:
        return HttpResponse("Invalid User")



def getMetricsList(object_list):
    m_list = []
    for o in object_list:
        m = o.setMetric()
        m_list.append(m)
    return m_list

def analysis(request, pid):
    p = Project.objects.filter(pk = pid)
    d_list = Developer.objects.filter(projects = p[0])
    pro_m_list = getMetricsList(p)
    ph_list = Phase.objects.filter(project = p).order_by('phase_id')
    pha_m_list = {}
    p_list = []
    for ph in ph_list:
        p_list.append(ph)
        it_list = Iteration.objects.filter(phase = ph)
        pha = getMetricsList([ph])[0]
        pha_m_list[pha] = getMetricsList(it_list)
    time_used = (ActivityTime.objects.filter(iteration = it_list).aggregate(Sum('time_used'))).values()
    context = {'name': request.user.username, 'ID': request.user.pk, 'time_used':time_used[0], 'developer_list': d_list, 'project': p[0], 'pro_m': pro_m_list, 'p_list': p_list, 'pha_m': pha_m_list}
    return render(request, 'pdt/analysis.html', context)

def delete_metrics_list(m_list):
    for m in m_list:
        m.delete()

def delete_metrics(o_list):
    for o in o_list:
        if isinstance(o, Project):
            m = Metrics.objects.filter(project = o)
            delete_metrics_list(m)
        elif isinstance(o, Phase):
            m = Metrics.objects.filter(phase = o)
            delete_metrics_list(m)
        else:
            m = Metrics.objects.filter(iteration = o)
            delete_metrics_list(m)

#Manager-view defect information-return defect data
def delete_project(request):
    pid = request.POST.get("pid")
    p = Project.objects.get(project_id = pid)
    ph_list = get_project_phase_list(pid)
    it_list = get_project_iteration_list(pid)
    delete_metrics(it_list)
    delete_metrics(ph_list)
    delete_metrics([p])
    p.delete()
    response = "Delete successfully."
    return HttpResponse(response)


def deleteIteration(it):
    delete_metrics([it])
    it.delete()

def newActivityTime(it, d):
    name_list = ['Development', 'Defect Removal', 'Management']
    for x in range(0,3):
        a = ActivityTime(iteration = it, developer = d, name = name_list[x])
        a.save()

def newPhase(pr1, it1, it2, it3, it4):
    it_num = [int(it1), int(it2), int(it3), int(it4)]
    ph_list = []
    for x in range(1, 5):
        ph = Phase(project = pr1, phase_id = x, num_of_iteration = it_num[x-1])
        ph.save()
        ph_list.append(ph)
    return ph_list

def newIteration(ph_list, pr1, developer_list):
    num = 0
    for ph in ph_list:
        num = int(ph.num_of_iteration)
        for x in range(1, num+1):
            it = Iteration(phase = ph, iteration_id = x)
            it.save()
            if ph == ph_list[0] and x == 1:
                pr1.current_ite = it
                pr1.save()
            for developer_id in developer_list:
                d = Developer.objects.filter(pk = developer_id)
                d[0].projects.add(pr1)
                newActivityTime(it, d[0])

def new_project(request):
    developer_list = Developer.objects.all()
    context = {'name': request.user.username, 'ID': request.user.pk, 'd_list': developer_list}
    return render(request, 'pdt/new_project.html', context)

def create_project(request):
    maxPid = (Project.objects.all().aggregate(Max('project_id'))).values()
    if maxPid[0] is None:
        p_id = 1
    else:
        p_id = maxPid[0] + 1
    p_name = request.POST.get("project_name")
    p_description = request.POST.get("project_description")
    it1 = request.POST.get("inception_num")
    it2 = request.POST.get("elaboration_num")
    it3 = request.POST.get("construction_num")
    it4 = request.POST.get("transition_num")
    #developer_list=[]
    developer_list = request.POST.getlist('developer_list[]')
    pr1 = Project(name = p_name, description = p_description, project_id = p_id)
    pr1.save()
    #Manager.projects.add(pr1)
    ph_list = newPhase(pr1, it1, it2, it3, it4)
    newIteration(ph_list, pr1, developer_list)
    return HttpResponse("Create successfully")

#Manager-edit project-display information for iterations that can be edited
def edit_project(request,pid):
    if request.user.is_authenticated():
        if request.user.groups.filter(name="Manager").exists():
            p = Project.objects.get(project_id = pid)
            possible_ph_list = Phase.objects.filter(project = p).filter(phase_id__gte = p.current_ite.phase.phase_id)
            delete_iteration_list = get_after_iteration(pid)
            context={'name': request.user.username, 'ID': request.user.pk, 'ph_list':possible_ph_list, 'delete_list': delete_iteration_list, 'pid': pid}
            return render(request, 'pdt/edit_project.html',context)
        else:
            return HttpResponse("Permission Denied")
    else:
        return HttpResponse("Invalid User")

#Manager-close iteration-set project's updated current iteration
def set_next_iteration(pid):
    p = Project.objects.get(project_id = pid)
    it_list = get_after_iteration(pid)
    if len(it_list) > 0:
        p.current_ite = it_list[0]
        p.save()
        return it_list[0]
    else:
        return "none"
#Manager-close iteration
def m_close_iteration(request, pid):
    next_it = set_next_iteration(pid)
    if next_it == "none":
        return HttpResponse("The whole project is closed successfully")
    else:
        return HttpResponse("The iteration is closed successfully")

#Manager-set code size-set code size for each iteration
def m_set_code_size(request):
    it_pk = request.POST.get("iteration_pk")
    code_size = request.POST.get("code_size")
    it = Iteration.objects.get(pk = it_pk)
    it.code_size = code_size
    it.save()
    return HttpResponse("Code size set successfully")

#Manager-delete_iteration-delete iteration to each phase
def delete_iteration(request):
    it_pk_list = []
    it_pk_list = request.POST.getlist("iteration_pk_list[]")
    for i in it_pk_list:
        it = Iteration.objects.get(pk = i)
        ph = it.phase
        ph.num_of_iteration -= 1
        ph.save()
        it.delete()  
    return HttpResponse("Delete successfully")

#Manager-add_iteration-add iteration to each phase
def add_iteration(request):
    ph_pk = request.POST.get("phase")
    add_num = request.POST.get("amount")
    phase = Phase.objects.get(pk = ph_pk)
    add_new_iteration(phase, int(add_num))
    return HttpResponse("Add iteration successfully" )

#Manager-add new iteration to phase
def add_new_iteration(phase, num):
    pro = phase.project
    developer_list = get_project_developer(pro.project_id)
    phase.num_of_iteration += num
    phase.save()
    for x in range(phase.num_of_iteration - num + 1, phase.num_of_iteration + 1):
        it = Iteration(phase = phase, iteration_id = x)
        it.save()
        for d in developer_list:
            newActivityTime(it, d)

#Manager-view project defects-return a list of project's defect
def m_view_defects(request, pid):
    d_list = get_project_developer(pid)
    it_list = get_project_iteration_list(pid)
    dd_list = DefectData.objects.filter(inject_iteration__in = it_list, developer__in = d_list)
    context = {'name': request.user.username, 'ID': request.user.pk, 'defect_list': dd_list}
    return render(request, 'pdt/view_defects.html', context)

#Manager-view defect information-return defect data
def m_view_defect_information(request, dpk):
    d = DefectData.objects.get(pk = dpk)
    context = {'name': request.user.username, 'ID': request.user.pk, 'defect': d}
    return render(request, 'pdt/defect_info_manager.html', context)


def new_development(request, pid):
    p = Project.objects.get(project_id = pid)
    cur_it = p.current_ite
    d = request.user.developer
    time = get_activity_time(pid, d, 'Defect Removal')
    dict = get_before_information(pid)
    possible_ph_list = list(dict.keys())
    it_num_list = list(dict.values())
    context = {'name': request.user.username, 'ID': request.user.pk, 'itnum_list': it_num_list, 'new_ph_list': possible_ph_list,'project': p, 'phase': cur_it.phase.get_phase_id_display(), 'phase_id': cur_it.phase.phase_id, 'iteration': cur_it.iteration_id, 'time_used': time}
    return render(request, 'pdt/defect_removal.html', context)    


def show_changelog(request):
    iid = request.POST.get("iid")
    activity_list = ActivityTime.objects.filter(iteration_id = iid)
    log_list = ChangeLog.objects.filter(activity = activity_list)
    string_list = []
    for log in log_list:
        activity = log.activity
        s = activity.developer.user.username + ' changes record #' + str(activity.pk) + ' ' + activity.name + ' from ' + str(log.originalTimeUsed) + 's to ' + str(log.updateTimeUsed) + 's at ' + log.occurTime.strftime('%Y-%m-%d %H:%M')
        string_list.appent(s)

    context = {}
    return 