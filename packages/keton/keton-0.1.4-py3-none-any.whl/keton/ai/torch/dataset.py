from typing import Any, Sequence, Optional, Callable, List

from torch.utils.data import Dataset, Subset


class Subset(Subset):

    def __init__(self, 
                 dataset: Dataset, 
                 indices: Sequence[int], 
                 transforms: Optional[List[Callable]] = None) -> None:
        super().__init__(dataset, indices)
        self.transforms = transforms

    def __getitem__(self, idx: Any) -> Any:
        item = super().__getitem__(idx)
        if self.transforms is None:
            return item
        if isinstance(item, (tuple, list)):
            if len(item) != len(self.transforms):
                raise ValueError("number of transforms should match with data size")
            return tuple(map(lambda i, t: t(i) if t is not None else i, item, self.transforms))
        else:
            if len(self.transforms) != 1:
                raise ValueError("number of transforms should match with data size")
            if self.transforms[0] is not None:
                return self.transforms[0](item) 
            return item

    def apply_transforms(self, transforms: List[Callable]) -> None:
        if not isinstance(transforms, (tuple, list)):
            raise ValueError("transforms must be a list or tuple")
        if len(transforms) != len(self[0]):
            raise ValueError("number of transforms should match with data size")
        self.transforms = transforms
