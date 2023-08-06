import csv
from abc import ABC, abstractmethod
from pathlib import Path

from pyPhases.util.Optionizable import Optionizable
from pyPhases.util.EventBus import EventBus

from .DataSet import DataSet


class MetricsDoesNotExist(Exception):
    pass

class AdapterNotImplemented(Exception):
    pass


class Model(ABC, Optionizable, EventBus):
    metrics = {
        "acc": {"name": "acc", "type": "max"},
        "binary_accuracy": {"name": "binary_accuracy", "type": "max"},
        "accuracy": {"name": "accuracy", "type": "max"},
        "kappa": {"name": "kappa", "type": "max"},
        "loss": {"name": "loss", "type": "min"},
    }
    optimizers = ["adams"]
    useGPU = True

    def __init__(self, options=None) -> None:
        options = options or {}
        super().__init__(options)
        self.logPath = "logs"
        self.csvLogFile = "log.csv"
        # segmentlength, channelSize
        self.inputShape = None
        self.numClasses = None
        self.classWeights = None

        self.batchSize = None
        self.maxEpochs = 100
        self.stopAfterNotImproving = None
        self.learningRate = 0.001
        self.learningRateDecay = None

        self.classNames = []
        self.monitorMetrics = ["accuracy"]
        self.optimizer = "adams"
        self.validationMetrics = ["kappa", "accuracy"]

        self.model = None
        self.modelEval = None
        self.modelDebug = None
        self.parameter = None
        self.bestMetric = 0
        self.fullEpochs = 0
        self.validationEvery = None
        self.ignoreClassIndex = -1

        self.startFigures = []
        self.showProgress = True
        self.startEpoch = 0
        self.useEventScorer = False
        self.predictionType = "classification"

        self.oneHotDecoded = False

    def getCsvPath(self):
        return f"{self.logPath}/{self.csvLogFile}"

    def getMetric(self, name):
        if name not in Model.metrics:
            raise MetricsDoesNotExist(f"The metrics with the name {name} is not defined")
        return Model.metrics[name]

    def init(self):
        pass

    def define(self):
        pass

    def prepareData(self, dataset: DataSet, validation=False):
        x, y = dataset
        return self.prepareX(x), self.prepareY(y)

    def prepareX(self, x, validation=False):
        return x

    def prepareY(self, y, validation=False):
        return y

    def beforeTrain(self, dataset):
        pass

    def model(self):
        pass

    def summary(self):
        self.logWarning("No summary implemented in the model adapter")

    def getLossFunction(self):
        raise AdapterNotImplemented("No loss function was specified in the model adapter!")

    def getLossWeights(self):
        return None

    def getModelEval(self):
        model = self.model if self.modelEval is None else self.modelEval
        model.eval()
        return model

    def getModelDebug(self):
        return self.model if self.modelDebug is None else self.modelDebug

    def mapOutput(self, outputData):
        return outputData

    def mapPrediction(self, output):
        return output

    def mapOutputForPrediction(self, output, mask=None):
        # batchsize, predictionsCounts, classcount
        return output

    def mapOutputForLoss(self, output, mask=None):
        return output

    def cleanUp(self):
        return

    def save(self, path):
        return

    @abstractmethod
    def train(self, dataset: DataSet, validationDataset: DataSet = None):
        raise AdapterNotImplemented("required train method is not implemented in the model adapter!")

    @abstractmethod
    def predict(self, input, get_likelihood=False, returnNumpy=True):
        raise AdapterNotImplemented("required predict method is not implemented in the model adapter!")
