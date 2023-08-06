from dataclasses import dataclass
from habil.sub.tag import HabiTag
from habil_base.exceptions import HabiRequestException
from habil_base.habiUItem import HabiUItem
import habil_case
from habil_base import token_required
import typing

@dataclass(frozen=True)
class AHabiTask(HabiUItem):
    createdAt : str
    updatedAt : str
    text : str
    tags : typing.List[str]
    _type = "task"

    def __post_init__(self):
        tag_objs = []
        for tag in self.tags:
            atag = HabiTag.get(id=tag)
            tag_objs.append(atag)
        object.__setattr__(self, "tags", tag_objs)

    def __repr__(self) -> str:
        return "{}({})".format(self.__class__.__name__, self.text)

    def __str__(self) -> str:
        return "{}({})".format(self.__class__.__name__, self.id)


    @classmethod
    @token_required()
    def get(cls, id : str, token=None, **kwargs):
        res = habil_case.task.get_a_task(headers=token, taskId=id, **kwargs)
        if not res.success:
            raise HabiRequestException(res)
        if res.type == cls._type:
            return cls.from_res(res)
        return None

    @token_required()
    def update(self, token=None,**kwargs)-> 'AHabiTask':
        res = habil_case.task.update_a_task(headers=token, taskId=self.id, **kwargs)
        if not res.success:
            raise HabiRequestException(res)
        created_obj = self.from_res(res)
        return created_obj

    @token_required()
    def delete(self, token=None, **kwargs) -> bool:
        res = habil_case.task.delete_a_task(headers=token, taskId=self.id, **kwargs)
        if not res.success:
            raise HabiRequestException(res)
        return True

    @token_required()
    def score_task(self,score: bool = True, token=None, **kwargs):
        res = habil_case.task.score_a_task(headers=token, taskId=self.id, direction="up" if score else "down", **kwargs)
        if not res.success:
            raise HabiRequestException(res)
        return self.get(id=self.id, token=token)

@dataclass(frozen=True)
class CompletableTask(AHabiTask):
    completed : bool
    checklist : typing.List[str]

    def __post_init__(self):
        super().__post_init__()
        pass

    @token_required()
    def complete(self, revert: bool = False, token=None) -> 'CompletableTask':
        if not isinstance(revert, bool):
            raise TypeError("revert must be bool")

        