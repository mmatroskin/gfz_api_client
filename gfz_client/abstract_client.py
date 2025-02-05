from abc import ABC, abstractmethod


class AbstractClient(ABC):
    """Abstract Client"""

    @abstractmethod
    def get_nowcast(self,
                    start_time: str,
                    end_time: str,
                    index: str,
                    data_state: str = "all") -> dict | None:
        """Get geomagnetic three-hourly Kp index for period from GFZ sources:
            https://kp.gfz-potsdam.de/
            https://kp.gfz-potsdam.de/hp30-hp60
        Args:
            start_time: start UCS time
            end_time: start UCS time
            index: name of Kp index
            data_state: string parameter 'status' for index
        Returns:
            Response as a dict.
        """

    def get_forecast(self, index: str) -> dict:
        """Get geomagnetic index forecast from GFZ sources:
            https://spaceweather.gfz.de/products-data/forecasts/forecast-kp-index
            https://spaceweather.gfz.de/products-data/forecasts/forecast-hp30-hp60-indices
        Args:
            index: name of Kp index
        Returns:
            Dict, contains index forecast data
        """

    @abstractmethod
    def get_kp_index(self,
                     starttime: str,
                     endtime: str,
                     index: str,
                     status: str = "all") -> tuple[tuple[str] | int, tuple[int] | int, tuple[str] | int]:
        """Get geomagnetic three-hourly Kp index for period as a tuple.
        Method implements getKpindex method from official python gfz_client (https://kp.gfz-potsdam.de/en/data)
        with same behaviour and added for compatibility purposes
        Args:
            starttime: start UCS time
            endtime: start UCS time
            index: name of Kp index
            status: optional string parameter 'status' for index
        Returns:
            Tuple with dates, Kp index values, index statuses
        """


class AbstractAsyncClient(ABC):
    """Abstract Async Client"""

    @abstractmethod
    async def get_nowcast(self,
                          start_time: str,
                          end_time: str,
                          index: str,
                          data_state: str = "all") -> dict:
        """Get geomagnetic three-hourly Kp index for period from GFZ sources:
            https://kp.gfz-potsdam.de/
            https://kp.gfz-potsdam.de/hp30-hp60
        Args:
            start_time: start UCS time
            end_time: start UCS time
            index: name of Kp index
            data_state: string parameter 'status' for index
        Returns:
            Dict, contains Kp index data for period
        """

    @abstractmethod
    async def get_forecast(self, index: str) -> dict:
        """Get geomagnetic index forecast from GFZ sources:
            https://spaceweather.gfz.de/products-data/forecasts/forecast-kp-index
            https://spaceweather.gfz.de/products-data/forecasts/forecast-hp30-hp60-indices
        Args:
            index: name of Kp index
        Returns:
            Dict, contains index forecast data
        """

    @abstractmethod
    async def get_kp_index(self,
                           starttime: str,
                           endtime: str,
                           index: str,
                           status: str = "all") -> tuple[tuple[str] | int, tuple[int] | int, tuple[str] | int]:
        """Get geomagnetic three-hourly Kp index for period as a tuple.
        Method implements getKpindex method from official python gfz_client (https://kp.gfz-potsdam.de/en/data)
        with same behaviour and added for compatibility purposes
        Args:
            starttime: start UCS time
            endtime: start UCS time
            index: name of Kp index
            status: optional string parameter 'status' for index
        Returns:
            Tuple with dates, Kp index values, index statuses
        """
