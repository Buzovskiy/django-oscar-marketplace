from oscar.core.application import OscarConfig
from django.urls import path, re_path
from oscar.core.loading import get_class


class InterviewConfig(OscarConfig):
    interview_start_view = interview_stage_view = interview_stage_02_view = None
    label = 'interview'
    name = 'application.interview'
    namespace = 'interview'

    def ready(self):
        self.interview_start_view = get_class('interview.views', 'InterviewStart')
        self.interview_stage_view = get_class('interview.views', 'InterviewStage')

    def get_urls(self):
        urls = [
            path('start/', self.interview_start_view.as_view(), name='start'),
            path('stage-01/', self.interview_stage_view.as_view(), {'stage_id': '01'}, name='stage_01'),
            path('stage-02/', self.interview_stage_view.as_view(), {'stage_id': '02'}, name='stage_02'),
            path('stage-03/', self.interview_stage_view.as_view(), {'stage_id': '03'}, name='stage_03'),
            path('stage-04/', self.interview_stage_view.as_view(), {'stage_id': '04'}, name='stage_04'),
            path('stage-05/', self.interview_stage_view.as_view(), {'stage_id': '05'}, name='stage_05'),
        ]
        return self.post_process_urls(urls)
