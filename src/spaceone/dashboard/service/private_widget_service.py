import logging
from typing import Union

from spaceone.core.service import *
from spaceone.core.error import *
from spaceone.dashboard.manager.private_widget_manager import PrivateWidgetManager
from spaceone.dashboard.manager.private_dashboard_manager import PrivateDashboardManager
from spaceone.dashboard.model.private_widget.request import *
from spaceone.dashboard.model.private_widget.response import *
from spaceone.dashboard.model.private_widget.database import PrivateWidget

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class PrivateWidgetService(BaseService):
    resource = "PrivateWidget"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pri_widget_mgr = PrivateWidgetManager()

    @transaction(
        permission="dashboard:PrivateWidget.write",
        role_types=["USER"],
    )
    @convert_model
    def create(
        self, params: PrivateWidgetCreateRequest
    ) -> Union[PrivateWidgetResponse, dict]:
        """Create private widget

        Args:
            params (dict): {
                'dashboard_id': 'str',          # required
                'name': 'str',
                'description': 'str',
                'widget_type': 'str',
                'options': 'dict',
                'tags': 'dict',
                'user_id': 'str',               # injected from auth (required)
                'domain_id': 'str',             # injected from auth (required)
            }

        Returns:
            PrivateWidgetResponse:
        """

        pri_dashboard_mgr = PrivateDashboardManager()
        pri_dashboard_mgr.get_private_dashboard(
            params.dashboard_id,
            params.domain_id,
            params.user_id,
        )

        pri_widget_vo = self.pri_widget_mgr.create_private_widget(params.dict())

        return PrivateWidgetResponse(**pri_widget_vo.to_dict())

    @transaction(
        permission="dashboard:PrivateWidget.write",
        role_types=["USER"],
    )
    @convert_model
    def update(
        self, params: PrivateWidgetUpdateRequest
    ) -> Union[PrivateWidgetResponse, dict]:
        """Update private widget

        Args:
            params (dict): {
                'widget_id': 'str',             # required
                'name': 'str',
                'description': 'str',
                'widget_type': 'str',
                'options': 'dict',
                'tags': 'dict',
                'user_id': 'str',               # injected from auth (required)
                'domain_id': 'str'              # injected from auth (required)
            }

        Returns:
            PrivateWidgetResponse:
        """

        pri_widget_vo = self.pri_widget_mgr.get_private_widget(
            params.widget_id,
            params.domain_id,
            params.user_id,
        )

        pri_widget_vo = self.pri_widget_mgr.update_private_widget_by_vo(
            params.dict(exclude_unset=True), pri_widget_vo
        )

        return PrivateWidgetResponse(**pri_widget_vo.to_dict())

    @transaction(
        permission="dashboard:PrivateWidget.write",
        role_types=["USER"],
    )
    @convert_model
    def delete(self, params: PrivateWidgetDeleteRequest) -> None:
        """Delete private widget

        Args:
            params (dict): {
                'widget_id': 'str',             # required
                'user_id': 'str',               # injected from auth (required)
                'domain_id': 'str'              # injected from auth (required)
            }

        Returns:
            None
        """

        pri_widget_vo = self.pri_widget_mgr.get_private_widget(
            params.widget_id,
            params.domain_id,
            params.user_id,
        )

        self.pri_widget_mgr.delete_private_widget_by_vo(pri_widget_vo)

    @transaction(
        permission="dashboard:PrivateWidget.write",
        role_types=["USER"],
    )
    @convert_model
    def load(self, params: PrivateWidgetLoadRequest) -> dict:
        """Load private widget

        Args:
            params (dict): {
                'widget_id': 'str',             # required
                'query': 'dict (spaceone.api.core.v1.TimeSeriesAnalyzeQuery)', # required
                'vars': 'dict',
                'user_id': 'str',               # injected from auth (required)
                'domain_id': 'str'              # injected from auth (required)
            }

        Returns:
            None
        """

        pri_widget_vo = self.pri_widget_mgr.get_private_widget(
            params.widget_id,
            params.domain_id,
            params.user_id,
        )

        # TODO: Implement load public widget

        return {
            "results": [],
            "total_count": 0,
        }

    @transaction(
        permission="dashboard:PrivateWidget.read",
        role_types=["USER"],
    )
    @convert_model
    def get(
        self, params: PrivateWidgetGetRequest
    ) -> Union[PrivateWidgetResponse, dict]:
        """Get private widget

        Args:
            params (dict): {
                'widget_id': 'str',             # required
                'user_id': 'str',               # injected from auth (required)
                'domain_id': 'str'              # injected from auth (required)
            }

        Returns:
            PrivateWidgetResponse:
        """

        pri_widget_vo = self.pri_widget_mgr.get_private_widget(
            params.widget_id,
            params.domain_id,
            params.user_id,
        )

        return PrivateWidgetResponse(**pri_widget_vo.to_dict())

    @transaction(
        permission="dashboard:PrivateWidget.read",
        role_types=["USER"],
    )
    @append_query_filter(
        [
            "dashboard_id",
            "widget_id",
            "name",
            "domain_id",
            "user_id",
        ]
    )
    @append_keyword_filter(["widget_id", "name"])
    @convert_model
    def list(
        self, params: PrivateWidgetSearchQueryRequest
    ) -> Union[PrivateWidgetsResponse, dict]:
        """List private widgets

        Args:
            params (dict): {
                'query': 'dict (spaceone.api.core.v1.Query)'
                'dashboard_id': 'str',                          # required
                'widget_id': 'str',
                'name': 'str',
                'user_id': 'str',                               # injected from auth (required)
                'domain_id': 'str',                             # injected from auth (required)
            }

        Returns:
            PrivateWidgetsResponse:
        """

        query = params.query or {}
        pri_widget_vos, total_count = self.pri_widget_mgr.list_private_widgets(query)
        pri_widgets_info = [pri_widget_vo.to_dict() for pri_widget_vo in pri_widget_vos]
        return PrivateWidgetsResponse(results=pri_widgets_info, total_count=total_count)