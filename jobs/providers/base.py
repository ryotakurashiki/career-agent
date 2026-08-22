from abc import ABC, abstractmethod
from jobs.models import Job


class JobProvider(ABC):
    """
    全Providerが実装すべきインターフェース。
    新しい求人ソースを追加するときはこのクラスを継承してsearchを実装する。
    """

    @abstractmethod
    def search(self, query: str, location: str, employment_type: str, limit: int) -> list[Job]:
        pass
