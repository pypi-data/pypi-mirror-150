from abc import ABC
from abc import abstractmethod
from datetime import timedelta

from tecton_proto.args import virtual_data_source_pb2


class BaseBatchConfig(ABC):
    @property
    @abstractmethod
    def data_delay(self) -> timedelta:
        pass

    @abstractmethod
    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        pass
