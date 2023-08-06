from .generic_service import GenericService
import pandas as pd
import os
from fileioutilities.file_io import FileIO
from bdaserviceutils import get_args
from dsioutilities import Dataset


class PandasService(GenericService):
    def __init__(self):
        super().__init__()

    def get_dataset(self):
        input_dataset = Dataset(name="input-dataset")

        # If list of csv concatenate them
        if isinstance(input_dataset.get_path(), list):
            df = pd.concat([pd.read_csv(filename) for filename in input_dataset.get_path()])
        else:
            df = pd.read_csv(input_dataset.get_path())
        return df

    def save_dataset(self, dataset: pd.DataFrame):
        dataset.to_csv(Dataset(name="output-dataset").get_path(), index=False)

    def download_model(self):
        path = os.path.join(".", "model")
        fileIO = FileIO(storage_type=self._args['dataStorageType-input-model'])
        fileIO.download(remote_path=get_args()['input-model'], local_path=path)
        return path

    def upload_model(self, path):
        fileIO = FileIO(storage_type=self._args['dataStorageType-output-model'])
        fileIO.upload(local_path=path, remote_path=self._args['output-model'])
