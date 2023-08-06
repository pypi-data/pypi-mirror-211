from abc import abstractmethod, ABC
from typing import Callable, List, Any, Dict, Optional, TypedDict

from glom import glom

from filum_utils.clients.action import ActionClient, ActionError
from filum_utils.clients.filum import FilumClient
from filum_utils.clients.log import LogClient, LogType
from filum_utils.clients.notification import (
    NotificationClient,
    PublisherType,
    RoutePath,
    NOTIFICATION_ERROR_MESSAGE_MAPPINGS,
)
from filum_utils.clients.subscription import SubscriptionClient
from filum_utils.config import config
from filum_utils.enums import ParentType, Object
from filum_utils.errors import BaseError


class TriggerFunctionResponse(TypedDict):
    is_finished: bool
    success_count: Optional[int]


ActionType = Dict[str, Any]
AutomatedActionType = Dict[str, Any]
CampaignType = Dict[str, Any]
EventType = Optional[Dict[str, Any]]
ObjectType = Optional[Dict[str, Any]]
UserType = Optional[Dict[str, Any]]
SubscriptionDataType = Optional[Dict[str, Any]]
ConnectionsType = Optional[List[Dict[str, Any]]]
OrganizationType = Dict[str, Any]


class BaseSubscriptionObjectClient(ABC):
    def __init__(self, subscription_id: int):
        self.subscription_client = SubscriptionClient(subscription_id)
        self.action_client = ActionClient(action_id=self.subscription_client.get_action_id())
        self.filum_client = FilumClient()
        self.log_client = LogClient()
        self.notification_client = NotificationClient()

    @property
    @abstractmethod
    def object(self):
        ...

    @property
    @abstractmethod
    def member_account_id(self):
        ...

    @property
    @abstractmethod
    def member_organization_id(self):
        ...

    @abstractmethod
    def get_run_type(self):
        ...

    def get_object_source_type(self):
        object_source = self.object.get("source") or {}
        return object_source.get("type")

    @abstractmethod
    def update_object_status(self, status: str):
        ...

    def get_action_data(self, key):
        return self.action_client.get_data(key)

    def update_action_data(self, updated_data: Dict[str, Any]):
        return self.action_client.update_data(updated_data)

    def get_subscription_data(self):
        return self.subscription_client.get_data()

    def update_subscription_data(self, updated_data: Dict[str, Any]):
        self.subscription_client.update_data(updated_data)

    @abstractmethod
    def handle_trigger_failed(self, error: ActionError, notify: bool):
        ...

    @abstractmethod
    def handle_transactional_trigger(
        self, process_transactional_fn: Callable, events: List[Dict[str, Any]]
    ) -> TriggerFunctionResponse:
        ...

    @abstractmethod
    def handle_segment_users_on_demand_trigger(
        self,
        process_segment_user_fn: Callable,
        properties: List[str] = None,
        required_properties: List[List[str]] = None,
        last_current_index: int = None
    ) -> TriggerFunctionResponse:
        ...

    @abstractmethod
    def handle_object_on_demand_trigger(self, process_segment_fn: Callable) -> TriggerFunctionResponse:
        ...

    @abstractmethod
    def _get_object_route(self):
        ...

    def _log(self, parent_type: str, type: str, code: str, title: str, subtitle: str, data: str = None):
        self.log_client.create_log(
            parent_type=parent_type,
            parent_id=self.object["id"],
            type=type,
            code=code,
            title=title,
            subtitle=subtitle,
            data=data,
            member_account_id=self.member_account_id,
            member_organization_id=self.member_organization_id,
        )

    def _notify(self, publisher_type: str, title: str, subtitle: str):
        self.notification_client.create_notification(
            publisher_type=publisher_type,
            title=title,
            subtitle=subtitle,
            route=self._get_object_route(),
            member_account_id=self.member_account_id,
            member_organization_id=self.member_organization_id,
        )


class AutomatedActionClient(BaseSubscriptionObjectClient):
    def __init__(self, subscription_id: int):
        super().__init__(subscription_id)
        self.automated_action = self.filum_client.get_automated_action(self.subscription_client.get_object_id())

    @property
    def object(self):
        return self.automated_action

    @property
    def member_account_id(self):
        creator = self.automated_action.get("creator") or {}
        account = creator.get("account") or {}
        return account.get("id")

    @property
    def member_organization_id(self):
        return self.automated_action.get("creator_organization_id")

    def get_run_type(self):
        return self.automated_action.get("run_type")

    def get_context_type(self):
        context = self.object.get("context") or {}
        return context.get("type")

    def get_context_id(self):
        context = self.object.get("context") or {}
        return context.get("id")

    def update_object_status(self, status: str):
        self.filum_client._request(
            endpoint=f"/internal/automated-actions/{self.automated_action['id']}/status",
            method="PUT",
            data={
                "status": status
            }
        )

    def handle_trigger_failed(self, error: ActionError, notify: bool):
        self._log(
            parent_type=ParentType.AUTOMATED_ACTION,
            type=LogType.ERROR,
            code="400",
            title="An error occurred when triggering your action, please contact Filum for support.",
            subtitle=error["message"],
            data=error["data"],
        )

        if notify:
            self._notify(
                publisher_type=PublisherType.AUTOMATED_ACTION,
                title=f"{self.automated_action.get('name')} failed to run",
                subtitle=error.get("notification_message") or NOTIFICATION_ERROR_MESSAGE_MAPPINGS[error["type"]],
            )

    def handle_transactional_trigger(
        self,
        process_transactional_fn: Callable[
            [ActionType, AutomatedActionType, EventType, SubscriptionDataType, ConnectionsType, OrganizationType],
            bool
        ],
        events: List[Dict[str, Any]],
        connections: List[Dict[str, Any]] = None,
        organization: Dict[str, Any] = None
    ) -> TriggerFunctionResponse:
        success_count = 0

        for event in events:
            result = self._handle_trigger(
                process_fn=process_transactional_fn,
                data=event,
                connections=connections,
                organization=organization
            )

            if result:
                success_count += 1

        return {
            "is_finished": True,
            "success_count": success_count
        }

    def handle_segment_users_on_demand_trigger(
        self,
        process_segment_user_fn: Callable[
            [ActionType, AutomatedActionType, UserType, SubscriptionDataType, ConnectionsType, OrganizationType],
            bool
        ],
        properties: List[str] = None,
        required_properties: List[List[str]] = None,
        last_current_index: int = None,
        connections: List[Dict[str, Any]] = None,
        organization: Dict[str, Any] = None
    ) -> TriggerFunctionResponse:
        if not last_current_index:
            last_current_index = 0

        subscription_data = self.get_subscription_data()
        current_index = subscription_data.get("last_current_index") or 0
        if current_index != last_current_index:
            raise BaseError(
                message="Last current index not matched",
                data={
                    "Automated Action ID": self.automated_action.get("id"),
                    "Current Index": current_index,
                    "Last Current Index": last_current_index
                }
            )

        users = self.filum_client.get_user_csv_reader(
            properties=properties,
            object_ids=[self.get_context_id()],
            object_type="segment",
            organization=self.subscription_client.get_organization(),
            required_properties=required_properties,
            offset=current_index,
            limit=config.SEGMENT_RECORD_LIMIT
        )

        total_processed_users = 0
        success_count = 0
        for user in users:
            current_index += 1
            total_processed_users += 1

            result = self._handle_trigger(
                process_fn=process_segment_user_fn,
                data=user,
                connections=connections,
                organization=organization
            )

            if result:
                success_count += 1

        if total_processed_users >= config.SEGMENT_RECORD_LIMIT:
            self.update_subscription_data({"last_current_index": current_index})
            self.action_client.sync({
                "subscription_id": self.subscription_client.subscription["id"],
                "last_current_index": last_current_index
            })

            return {
                "is_finished": False,
                "success_count": success_count
            }

        return {
            "is_finished": True,
            "success_count": success_count
        }

    def handle_object_on_demand_trigger(
        self,
        process_segment_fn: Callable[
            [ActionType, AutomatedActionType, ObjectType, SubscriptionDataType, ConnectionsType, OrganizationType],
            bool
        ],
        connections: List[Dict[str, Any]] = None,
        organization: Dict[str, Any] = None
    ) -> TriggerFunctionResponse:

        context_type = self.get_context_type()

        data = {}
        if context_type == Object.SEGMENT:
            data = self.filum_client.get_segment(
                segment_id=self.get_context_id(),
                organization=self.subscription_client.get_organization()
            )
        elif context_type == Object.CAMPAIGN:
            data = self.filum_client.get_campaign(campaign_id=self.get_context_id())

        result = self._handle_trigger(
            process_fn=process_segment_fn,
            data=data,
            connections=connections,
            organization=organization
        )

        success_count = 1 if result else 0

        return {
            "is_finished": True,
            "success_count": success_count
        }

    def _handle_trigger(
        self,
        process_fn: Callable,
        data: Dict[str, Any],
        connections: List[Dict[str, Any]] = None,
        organization: Dict[str, Any] = None
    ):
        if not connections:
            connections = []

        params = {
            "action": self.action_client.action,
            "automated_action": self.automated_action,
            "data": data,
            "subscription_data": self.get_subscription_data(),
            "connections": connections,
            "organization": organization
        }

        return process_fn(**params)

    def _get_object_route(self):
        return {
            "path": RoutePath.AUTOMATED_ACTIONS_DETAIL,
            "params": {
                "automatedActionId": self.automated_action["id"]
            }
        }


class CampaignClient(BaseSubscriptionObjectClient):
    def __init__(self, subscription_id: int):
        super().__init__(subscription_id)
        self.campaign = self.filum_client.get_campaign(self.subscription_client.get_object_id())

    @property
    def object(self):
        return self.campaign

    @property
    def member_account_id(self):
        creator = self.campaign.get("creator") or {}
        account = creator.get("account") or {}
        return account.get("id")

    @property
    def member_organization_id(self):
        return self.campaign.get("creator_organization_id")

    def get_run_type(self):
        return self.campaign.get("run_type")

    def get_segment_id(self):
        return self.campaign.get("segment_id")

    def get_template(self):
        campaign_survey = self.object and self.object.get("survey")
        action_id = self.action_client.action['id']

        template = glom(campaign_survey, f"action_data.{action_id}", default=None)
        if not template:
            template = glom(self.object, f"action_input_data.{action_id}", default=None)

        if template and template["status"] == "active":
            return template

        return None

    def get_template_third_party_id(self):
        template = self.get_template()
        return template and template.get("third_party_id")

    def update_object_status(self, status: str):
        self.filum_client._request(
            endpoint=f"/internal/survey-campaigns/{self.campaign['id']}/status",
            method="PUT",
            data={
                "status": status
            }
        )

    def handle_trigger_failed(self, error: ActionError, notify: bool = False):
        self._log(
            parent_type=ParentType.CAMPAIGN,
            type=LogType.ERROR,
            code="400",
            title="An error occurred when triggering your action, please contact Filum for support.",
            subtitle=error["message"],
            data=error["data"],
        )

        if notify:
            self._notify(
                publisher_type=PublisherType.FEEDBACK_360,
                title=f"{self.campaign.get('name')} failed to run",
                subtitle=error.get("notification_message") or NOTIFICATION_ERROR_MESSAGE_MAPPINGS[error["type"]],
            )

    def handle_transactional_trigger(
        self,
        process_transactional_fn: [
            [ActionType, CampaignType, EventType, SubscriptionDataType, ConnectionsType],
            bool
        ],
        events: List[Dict[str, Any]],
        connections: List[Dict[str, Any]] = None
    ) -> TriggerFunctionResponse:
        success_count = 0

        for event in events:
            result = self._handle_trigger(
                process_fn=process_transactional_fn,
                data=event,
                connections=connections
            )

            if result:
                success_count += 1

        return {
            "is_finished": True,
            "success_count": success_count
        }

    def handle_segment_users_on_demand_trigger(
        self,
        process_segment_user_fn: [
            [ActionType, CampaignType, UserType, SubscriptionDataType, ConnectionsType],
            bool
        ],
        properties: List[str] = None,
        required_properties: List[List[str]] = None,
        connections: List[Dict[str, Any]] = None,
        last_current_index: int = None,
        dedup_key: str = None
    ) -> TriggerFunctionResponse:
        if not last_current_index:
            last_current_index = 0

        subscription_data = self.get_subscription_data()
        current_index = subscription_data.get("last_current_index") or 0
        if current_index != last_current_index:
            raise BaseError(
                message="Last current index not matched",
                data={
                    "Campaign ID": self.campaign.get("id"),
                    "Current Index": current_index,
                    "Last Current Index": last_current_index
                }
            )

        users = self.filum_client.get_user_csv_reader(
            properties=properties,
            object_ids=[self.get_segment_id()],
            object_type="segment",
            organization=self.subscription_client.get_organization(),
            required_properties=required_properties,
            offset=current_index,
            limit=config.SEGMENT_RECORD_LIMIT
        )

        total_processed_users = 0
        success_count = 0
        dedup_values = set()

        for user in users:
            dedup_value = user.get(dedup_key) if dedup_key else None
            if dedup_value and dedup_value in dedup_values:
                continue

            if dedup_value:
                dedup_values.add(dedup_value)

            current_index += 1
            total_processed_users += 1
            result = self._handle_trigger(
                process_fn=process_segment_user_fn,
                data=user,
                connections=connections
            )
            if result:
                success_count += 1

        if total_processed_users >= config.SEGMENT_RECORD_LIMIT:
            self.update_subscription_data({"last_current_index": current_index})
            self.action_client.sync({
                "subscription_id": self.subscription_client.subscription["id"],
                "last_current_index": current_index
            })

            return {
                "is_finished": False,
                "success_count": success_count
            }

        return {
            "is_finished": True,
            "success_count": success_count
        }

    def handle_object_on_demand_trigger(self, process_segment_fn: Callable) -> TriggerFunctionResponse:
        ...

    def _handle_trigger(self, process_fn: Callable, data: Dict[str, Any], connections: List[Dict[str, Any]] = None):
        if not connections:
            connections = []

        params = {
            "action": self.action_client.action,
            "campaign": self.campaign,
            "data": data,
            "subscription_data": self.get_subscription_data(),
            "connections": connections
        }

        return process_fn(**params)

    def _get_object_route(self):
        return {
            "path": RoutePath.CAMPAIGNS_DETAIL,
            "params": {
                "solutionGroup": "cx",
                "solutionId": "dynamic_feedback",
                "campaignId": self.campaign["id"]
            }
        }
