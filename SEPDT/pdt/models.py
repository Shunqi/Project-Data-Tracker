from django.db import models
from django.db.models import Count, Min, Sum, Avg, Max
from datetime import timedelta
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    project_id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length=20, unique = True)
    description = models.CharField(max_length = 60)
    current_ite = models.ForeignKey('Iteration', default = 1, null=True, blank=True)
    metrics = models.ForeignKey('Metrics', default = 1, null=True, blank=True)
    def __str__(self):              # __str__ on Python 2
        return self.name
    def setMetric(self):
        m = Metrics().calculateMetrics(self)
        self.metrics = m
        self.save()
        return m

    def display_managers(self):
        return ', '.join([ manager.username for manager in self.managers.all() ])
    display_managers.short_description = 'Managers'
    display_managers.allow_tags = True

    def display_developers(self):
        return ', '.join([ developer.username for developer in self.developers.all() ])
    display_developers.short_description = 'Developers'
    display_developers.allow_tags = True

class Phase(models.Model):
    PHASE_NAME = (
                  (1, 'Inception'),
                  (2, 'Elaboration'),
                  (3, 'Construction'),
                  (4, 'Transition'),
                  )
    project = models.ForeignKey('Project')
    phase_id = models.IntegerField(default=1, choices=PHASE_NAME)
    num_of_iteration = models.IntegerField()
    metrics = models.ForeignKey('Metrics', default = 1, null=True, blank=True)
    def __str__(self):              # __str__ on Python 2
        return self.get_phase_id_display()
    def setMetric(self):
        m = Metrics().calculateMetrics(self)
        self.metrics = m
        self.save()
        return m

class Iteration(models.Model):
    phase = models.ForeignKey('Phase')
    iteration_id = models.IntegerField(default = 1)
    code_size = models.IntegerField(default = 0)
    metrics = models.ForeignKey('Metrics', default = 1, null=True, blank=True)
    def __str__(self):              # __str__ on Python 2
        return str(self.iteration_id)
    def setMetric(self):
        m = Metrics().calculateMetrics(self)
        self.metrics = m
        self.save()
        return m

class Manager(models.Model):
    user = models.OneToOneField(User)
    #employee_id = models.IntegerField(primary_key = True)
    #name = models.CharField(max_length=20)
    projects = models.ManyToManyField(Project, blank = True, related_name = 'managers')
    def __str__(self):              # __str__ on Python 2
        return self.user.username

    def display_projects(self):
        return ', '.join([ project.name for project in self.projects.all() ])
    display_projects.short_description = 'Projects'
    display_projects.allow_tags = True

class Developer(models.Model):
    user = models.OneToOneField(User)
    #employee_id = models.IntegerField(primary_key = True)
    #name = models.CharField(max_length=20)
    projects = models.ManyToManyField(Project, blank = True, related_name = 'developers')
    def __str__(self):              # __str__ on Python 2
        return self.user.username

    def display_projects(self):
        return ', '.join([ project.name for project in self.projects.all() ])
    display_projects.short_description = 'Projects'
    display_projects.allow_tags = True


class ActivityTime(models.Model):
    iteration = models.ForeignKey('Iteration')
    developer = models.ForeignKey('Developer')
    name = models.CharField(default='Development',max_length=20)
    time_used = models.IntegerField(default=0)
    starttime = models.DateTimeField('Start time')
    def __str__(self):              # __str__ on Python 2
        return self.name
    def get_time(self):
        return self.time_used
    def update_time(self, new_time):
        self.time_used = new_time
        self.save()

#more clrification needed
class ChangeLog(models.Model):
    activity = models.ForeignKey('ActivityTime')
    occurTime = models.DateTimeField('Establish time')
    originalTimeUsed = models.IntegerField('Former Time Used')
    updateTimeUsed = models.IntegerField('Updated Time Used')


class DefectData(models.Model):
    DATA_TYPE = (
                 ('R', 'Requirement'),
                 ('D', 'Design'),
                 ('I', 'Implementation'),
                 ('B', 'Bad fix'),
                 )
    inject_iteration = models.ForeignKey('Iteration', related_name = 'defectdata_inject_iteration')
    remove_iteration = models.ForeignKey('Iteration', related_name = 'defectdata_remove_iteration')
    developer = models.ForeignKey('Developer')
    data_type = models.CharField(max_length=1, choices=DATA_TYPE)
    description = models.CharField(max_length=200, default = '')
    def __str__(self):              # __str__ on Python 2
        return self.get_data_type_display()

class Metrics(models.Model):
    name = models.CharField(default='myName',max_length=20)
    SLOC = models.DecimalField(default=-1, max_digits = 10, decimal_places=3)
    effort = models.DecimalField(default=-1, max_digits = 10, decimal_places=3)
    code_effort = models.DecimalField(default=0, max_digits = 10, decimal_places=3)
    inject_num = models.IntegerField(default = 0)
    remove_num = models.IntegerField(default = 0)
    inject_rate = models.DecimalField(default=0, max_digits = 10, decimal_places=3)
    remove_rate = models.DecimalField(default=0, max_digits = 10, decimal_places=3)
    defect_density = models.DecimalField(default=0, max_digits = 10, decimal_places=3)
    m_yield = models.DecimalField(default=0, max_digits = 10, decimal_places=3)
    def __str__(self):              # __str__ on Python 2
        return self.name
    def newMetrics(self, n, S, e, ce, inj, rem, inr, rer, dd, y):
        self.name = n
        self.SLOC = S
        self.effort = e
        self.code_effort = ce
        self.inject_num = inj
        self.remove_num = rem
        self.inject_rate = inr
        self.remove_rate = rer
        self.defect_density = dd
        self.m_yield = y
        self.save()
        return self
    def calculateMetrics(self, o):
        it_list = []
        p_it_list = []
        name = ''
        if isinstance(o, Project):
            pro = o
            ph_list = Phase.objects.filter(project = pro)
            it_list = Iteration.objects.filter(phase = ph_list)
            name = o.name
        elif isinstance(o, Phase):
            pro = o.project
            it_list = Iteration.objects.filter(phase = o)
            name = o.get_phase_id_display()
        else:
            pha = o.phase
            pro = pha.project
            it_list = Iteration.objects.filter(iteration_id = o.iteration_id, phase = o.phase)
            name = str(o.iteration_id)
        p_it_list = Iteration.objects.filter(phase = Phase.objects.filter(project = pro))
        
        my_code_size = 0
        p_code_size = 0
        for it in it_list:
            my_code_size += it.code_size
        for it in p_it_list:
            p_code_size += it.code_size
        if p_code_size != 0:
            SLOC = my_code_size * 100/ p_code_size
        else:
            SLOC = 0

        my_time = (ActivityTime.objects.filter(iteration = it_list).aggregate(Sum('time_used'))).values()
        p_time = ActivityTime.objects.filter(iteration = p_it_list).aggregate(Sum('time_used')).values()
        developer_num = Developer.objects.filter(projects = pro).count()
        my_effort = my_time[0] * 100 / float(30 * 24 * 60 * 60) / developer_num
        p_effort = p_time[0] * 100 / float(30 * 24 * 60 * 60) / developer_num
        if p_effort != 0:
            effort = my_effort / p_effort
        else:
            effort = 0
        if effort == 0:
            code_effort = 0
        else:
            code_effort = my_code_size / float(my_effort)
        
        my_in_num = DefectData.objects.filter(inject_iteration = it_list).count()
        my_re_num = DefectData.objects.filter(remove_iteration = it_list).count()
        
        hour_effort = my_time[0] / 60 / 60
        my_in_rate = 0
        my_re_rate = 0
        my_density = 0
        if hour_effort != 0:
            my_in_rate = my_in_num * 100 / hour_effort
            my_re_rate = my_re_num * 100 / hour_effort
        if my_code_size != 0:
            my_density = my_in_num * 100 / float(my_code_size) * 1000

        if isinstance(o, Iteration):
            past_phase_list = Phase.objects.filter(project = pro).filter(phase_id__lt = pha.phase_id)
            past_iteration_list = Iteration.objects.filter(phase = past_phase_list)
            this_iteration_list = Iteration.objects.filter(phase = pha).filter(iteration_id__lt = o.iteration_id)
            all_but_me_iteration_list = past_iteration_list | this_iteration_list
            all_iteration_list = list(all_but_me_iteration_list) + [o]
        elif isinstance(o, Phase):
            past_phase_list = Phase.objects.filter(phase_id__lt = o.phase_id)
            past_iteration_list = Iteration.objects.filter(phase = past_phase_list)
            this_iteration_list = Iteration.objects.filter(phase = o)
            all_but_me_iteration_list = past_iteration_list
            all_iteration_list = all_but_me_iteration_list | this_iteration_list
        else:
            all_iteration_list = it_list
            all_but_me_iteration_list = []

        all_remove_num = DefectData.objects.filter(inject_iteration__in = all_iteration_list).count()
        last_remove_num = DefectData.objects.filter(remove_iteration = pro.current_ite).filter(inject_iteration__in = all_iteration_list).count()
        last_but_me_remove_num = DefectData.objects.filter(remove_iteration__in = all_but_me_iteration_list, inject_iteration__in = all_but_me_iteration_list).count()
        fenmu = all_remove_num + 0.25 * last_remove_num - last_but_me_remove_num
        if fenmu != 0:
            my_yield = my_re_num * 100 / float(fenmu)
        else:
            my_yield = 0

        return self.newMetrics(name, round(SLOC,2), round(effort,2) , round(code_effort,2), my_in_num, my_re_num, round(my_in_rate,2), round(my_re_rate,2), round(my_density,5), round(my_yield,2))
