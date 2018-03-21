from django.contrib import admin
from .models import Project, Phase, Iteration, ActivityTime, DefectData, Developer, Manager, Metrics, ChangeLog
from django.contrib.auth.models import User

class IterationInline(admin.TabularInline):
    model = Iteration
    extra = 0
    
class PhaseInline(admin.TabularInline):
    model = Phase
    inlines = [IterationInline]
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'project_id', 'description', 'display_managers', 'display_developers')
    inlines = [PhaseInline]

class PhaseAdmin(admin.ModelAdmin):
    list_display = ('get_project', 'phase_id', 'num_of_iteration')
    inlines = [IterationInline]
    fieldsets = [
        ('Project', {'fields': ['project']}),
        ('Phase', {'fields': ['phase_id', 'num_of_iteration']}),
    ]
    def get_project(self, obj):
        return obj.project.name
    get_project.short_description = 'Project'
    get_project.admin_order_field = '-project__project_id'

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0

class IterationAdmin(admin.ModelAdmin):
    list_display = ('get_project', 'get_phase', 'iteration_id', 'code_size')
    fieldsets = [
        ('Project and Phase', {'fields': ['phase']}),
        ('Iteration', {'fields': ['iteration_id', 'code_size']}),
    ]
    inlines = [ProjectInline]

    def get_project(self, obj):
        return obj.phase.project.name
    get_project.short_description = 'Project'
    get_project.admin_order_field = '-phase__project__project_id'

    def get_phase(self, obj):
        return obj.phase.get_phase_id_display()
    get_phase.short_description = 'Phase'
    get_phase.admin_order_field = '-phase__phase'


class ActivityTimeAdmin(admin.ModelAdmin):
	list_display = ('get_project', 'get_phase', 'get_iteration', 'name', 'time_used')
	fieldsets = [
    	('Project, Phase and Iteration', {'fields': ['iteration']}),
        ('ActivityTime', {'fields': ['name', 'time_used']}),
    ]

	def get_project(self, obj):
		return obj.iteration.phase.project.name
	get_project.short_description = 'Project'
	get_project.admin_order_field = '-phase__project__project_id'

	def get_phase(self, obj):
		return obj.iteration.phase.get_phase_id_display()
	get_phase.short_description = 'Phase'
	get_phase.admin_order_field = '-phase__phase'

	def get_iteration(self, obj):
		return obj.iteration.iteration_id
	get_iteration.short_description = 'Iteration'
	get_iteration.admin_order_field = '-iteration__iteration_id'

class DefectDataAdmin(admin.ModelAdmin):
	list_display = ('get_project', 'get_phase', 'get_inject_iteration', 'get_remove_iteration', 'get_developer', 'data_type', 'description')
	fieldsets = [
    	('Project, Phase and Iteration', {'fields': ['inject_iteration', 'remove_iteration']}),
        ('DefectData', {'fields': ['data_type', 'description']}),
    ]

	def get_project(self, obj):
		return obj.inject_iteration.phase.project.name
	get_project.short_description = 'Project'
	get_project.admin_order_field = '-inject_iteration__phase__project__project_id'

	def get_phase(self, obj):
		return obj.inject_iteration.phase.get_phase_id_display()
	get_phase.short_description = 'Phase'
	get_phase.admin_order_field = '-inject_iteration__phase__phase'

	def get_inject_iteration(self, obj):
		return obj.inject_iteration.iteration_id
	get_inject_iteration.short_description = 'Inject Iteration'
	get_inject_iteration.admin_order_field = '-inject_iteration__iteration_id'

	def get_remove_iteration(self, obj):
		return obj.remove_iteration.iteration_id
	get_remove_iteration.short_description = 'Remove Iteration'
	get_remove_iteration.admin_order_field = '-remove_iteration__iteration_id'

	def get_developer(self, obj):
		return obj.developer
	get_developer.short_description = 'Report Developer'
	get_developer.admin_order_field = '-developer__employee_id'

class DeveloperAdmin(admin.ModelAdmin):
	list_display = ('user', 'display_projects')

class ManagerAdmin(admin.ModelAdmin):
	list_display = ('user', 'display_projects')

class ChangeLogAdmin(admin.ModelAdmin):
	list_display = ('pk', 'time')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Phase, PhaseAdmin)
admin.site.register(Iteration, IterationAdmin)
admin.site.register(ActivityTime, ActivityTimeAdmin)
admin.site.register(DefectData, DefectDataAdmin)
admin.site.register(Developer, DeveloperAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(ChangeLog, ChangeLogAdmin)