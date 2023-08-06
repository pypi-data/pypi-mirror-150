from abc import ABC
from abc import abstractmethod


class ReflectionClassUtilsInterface(ABC):

    @staticmethod
    @abstractmethod
    def get_sub_packages(parent_package: str) -> list:
        pass

    @classmethod
    @abstractmethod
    def get_class_from_package(cls, parent_package: str, class_name: str):
        pass

    @classmethod
    @abstractmethod
    def get_class_filter_parent(cls, parent_package: str, parent_class: str) -> list:
        pass
