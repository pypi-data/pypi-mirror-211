from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.background_task_status import BackgroundTaskStatus
from ..models.background_task_type import BackgroundTaskType

T = TypeVar("T", bound="ReplayOut")


@attr.s(auto_attribs=True)
class ReplayOut:
    """
    Attributes:
        id (str):
        status (BackgroundTaskStatus):
        task (BackgroundTaskType):
    """

    id: str
    status: BackgroundTaskStatus
    task: BackgroundTaskType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        status = self.status.value

        task = self.task.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
                "task": task,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        dict_copy = src_dict.copy()
        id = dict_copy.pop("id")

        status = BackgroundTaskStatus(dict_copy.pop("status"))

        task = BackgroundTaskType(dict_copy.pop("task"))

        replay_out = cls(
            id=id,
            status=status,
            task=task,
        )

        replay_out.additional_properties = dict_copy
        return replay_out

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
