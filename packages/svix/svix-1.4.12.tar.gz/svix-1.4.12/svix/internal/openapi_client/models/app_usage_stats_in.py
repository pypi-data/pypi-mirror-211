import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="AppUsageStatsIn")


@attr.s(auto_attribs=True)
class AppUsageStatsIn:
    """
    Attributes:
        since (datetime.datetime):
        until (datetime.datetime):
        app_ids (Union[Unset, None, List[str]]):
    """

    since: datetime.datetime
    until: datetime.datetime
    app_ids: Union[Unset, None, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        since = self.since.isoformat()

        until = self.until.isoformat()

        app_ids: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.app_ids, Unset):
            if self.app_ids is None:
                app_ids = None
            else:
                app_ids = self.app_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "since": since,
                "until": until,
            }
        )
        if app_ids is not UNSET:
            field_dict["appIds"] = app_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        dict_copy = src_dict.copy()
        since = isoparse(dict_copy.pop("since"))

        until = isoparse(dict_copy.pop("until"))

        app_ids = cast(List[str], dict_copy.pop("appIds", UNSET))

        app_usage_stats_in = cls(
            since=since,
            until=until,
            app_ids=app_ids,
        )

        app_usage_stats_in.additional_properties = dict_copy
        return app_usage_stats_in

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
