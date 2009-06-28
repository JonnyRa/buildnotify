class ProjectStatusNotification:
    def __init__(self, old_projects, current_projects, notification):
        self.project_status = ProjectStatus(old_projects, current_projects)
        self.notification = notification

    def show_notifications(self):
        self.show_notification_msg(self.project_status.successful_builds(), "Fixed builds")
        self.show_notification_msg(self.project_status.failing_builds(), "Broken builds")
        self.show_notification_msg(self.project_status.still_failing_builds(), "Build is still failing")
        #self.show_notification_msg(self.project_status.still_successful_builds(), "Yet another successful build")
    
    def show_notification_msg(self, builds, message):
        if builds == []:
            return
        self.notification.update(message, "\n".join(builds), None)
        if not self.notification.show():
            print "Failed to send notification."
            gtk.main_quit()
        
class ProjectStatus:
    def __init__(self, old_projects, current_projects): 
        self.old_projects = old_projects
        self.current_projects = current_projects
    
    def failing_builds(self):
        return self.filter_all(lambda project_tuple: project_tuple.has_failed())

    def successful_builds(self):
        return self.filter_all(lambda project_tuple: project_tuple.has_succeeded())

    def still_failing_builds(self):
        return self.filter_all(lambda project_tuple: project_tuple.has_been_failing())

    def still_successful_builds(self):
        return self.filter_all(lambda project_tuple: project_tuple.has_been_successful())
    
    def filter_all(self, filter_fn):
        project_tuples = map(lambda current_project: self.tuple_for(current_project), self.current_projects.all_projects)
        project_tuples = filter(filter_fn, project_tuples)
        return map(lambda project_tuple: project_tuple.current_project.name, project_tuples)
               
    def tuple_for(self, new_project):
        for project in self.old_projects.all_projects:
            if project.name == new_project.name:
                return ProjectTuple(new_project, project)
        return ProjectTuple(new_project, None)
    
class ProjectTuple:
    def __init__(self, current_project, old_project):
        self.current_project = current_project
        self.old_project = old_project
    def has_failed(self):
        return self.status('Failure','Success')
    def has_succeeded(self):
        return self.status('Success','Failure')
    def has_been_successful(self):
        return self.status('Success','Success') and self.different_builds()
    def has_been_failing(self):
        return self.status('Failure','Failure') and self.different_builds()
    def status(self, new_status, old_status):
        return self.current_project.status == new_status and self.old_project.status == old_status
    def different_builds(self):
        return self.current_project.lastBuildTime != self.old_project.lastBuildTime    
        
        
        