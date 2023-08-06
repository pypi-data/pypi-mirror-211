import numpy as np


class DatasetXY:
    def __init__(self, dataExporterSignals, dataExporterFeatures):
        self.dataExporterSignals = dataExporterSignals
        self.dataExporterFeatures = dataExporterFeatures
        self.segmentMapping = None

    def __len__(self):
        return len(self.dataExporterSignals)

    def __getitem__(self, idx):
        segmentX, segmentY = self.dataExporterSignals[idx], self.dataExporterFeatures[idx]
        # convert to numpy arrays
        return np.array(segmentX), np.array(segmentY)

    def __iter__(self) -> int:
        for i in range(len(self)):
            yield self[i]
