class RecordMap:
    def __init__(self, dataset, mapping):
        self.dataset = dataset
        self.mapping = mapping
        self.currentIndex = 0

    def __len__(self):
        return len(self.mapping)

    def __getitem__(self, index):
        return self.dataset[self.mapping[index]]

    def __iter__(self) -> int:
        for i in range(len(self)):
            yield self[i]
