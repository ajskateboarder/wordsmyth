from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data import Data


T = TypeVar("T", bound="Output")


@attr.s(auto_attribs=True)
class Output:
    """
    Attributes:
        status (str):
        message (str):
        data (Union[Unset, Data]):
    """

    status: str
    message: str
    data: Union[Unset, "Data"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        message = self.message
        data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "message": message,
            }
        )
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.data import Data

        d = src_dict.copy()
        status = d.pop("status")

        message = d.pop("message")

        _data = d.pop("data", UNSET)
        data: Union[Unset, Data]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = Data.from_dict(_data)

        output = cls(
            status=status,
            message=message,
            data=data,
        )

        output.additional_properties = d
        return output

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
