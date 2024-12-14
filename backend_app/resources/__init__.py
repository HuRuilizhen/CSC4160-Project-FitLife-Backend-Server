from .login import LoginResource
from .register import RegisterResource
from .settings import SettingsResource
from .token_refresh import TokenRefreshResource
from .token_check import TokenCheckResource
from .dashboard_fetch import DashboardFetchResource
from .post_create import PostCreateResource
from .post_fetch import PostFetchResource
from .post_detail import PostDetailResource
from .post_update import PostUpdateResource
from .post_delete import PostDeleteResource
from .comment_create import CommentCreateResource
from .comment_delete import CommentDeleteResource
from .diet_record_fetch import DietRecordFetchResource
from .diet_record_create import DietRecordCreateResource
from .activity_record_create import ActivityRecordCreateResource
from .activity_record_fetch import ActivityRecordFetchResource
from .report_chart_fetch import ReportChartFetchResource


__all__ = [
    "LoginResource",
    "RegisterResource",
    "SettingsResource",
    "TokenRefreshResource",
    "TokenCheckResource",
    "DashboardFetchResource",
    "PostCreateResource",
    "PostFetchResource",
    "PostDetailResource",
    "PostUpdateResource",
    "PostDeleteResource",
    "CommentCreateResource",
    "CommentDeleteResource",
    "DietRecordFetchResource",
    "DietRecordCreateResource",
    "ActivityRecordCreateResource",
    "ActivityRecordFetchResource",
    "ReportChartFetchResource",
]
