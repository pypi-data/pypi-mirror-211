
from ..DataAugmentation import DataAugmentation


class Augmentor:
    def __init__(self, datapipe, augmentation: DataAugmentation, config) -> None:
        self.datapipe = datapipe
        self.augmentation = augmentation
        self.config = config

    def __getitem__(self, index):
        X, Y = self.augmentation(self.datapipe[index], self.config, index)
        return X.squeeze(0), Y.squeeze(0)

    def __len__(self):
        return len(self.datapipe)

