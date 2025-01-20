import logging

from gfz_client.abstract_client import AbstractClient, AbstractAsyncClient
from gfz_client.backends import HTTPBackend, HTTPAsyncBackend
from gfz_client import settings, utils, exceptions, types


logger = logging.getLogger("gfz_client")


class CommonGFZClient:
    """Common GFZ gfz_client methods and properties"""
    _forecast_link: str = settings.FORECAST_LINK
    _nowcast_link: str = settings.NOWCAST_LINK
    _ERROR_MESSAGE_FIELD: str = "message"
    _state_indices: tuple[str] = settings.STATE_INDEX_LIST

    def _get_params(self, start_time: str, end_time: str, index: str, data_state: str) -> dict:
        """Get query params"""
        utils.check_index_name(index)
        utils.check_status(data_state)
        start = utils.from_date_string(start_time)
        end = utils.from_date_string(end_time)
        utils.check_date(start, end)
        params = {
            "start": utils.to_date_string(start),
            "end": utils.to_date_string(end),
            "index": index,
        }
        if index in settings.STATE_INDEX_LIST:
            utils.check_status(data_state)
            params["status"] = data_state
        return params

    def _get_forecast_url(self, index: types.IndexType) -> str:
        """Build forecast url or raise Error"""
        match index:
            case types.IndexType.Kp:
                return self._forecast_link + settings.FORECAST_KP_PATH
            case types.IndexType.Hp30:
                return self._forecast_link + settings.FORECAST_HP3_PATH
            case types.IndexType.Hp60:
                return self._forecast_link + settings.FORECAST_HP6_PATH
            case _:
                raise exceptions.InternalServiceError("Malformed parameter on input")

    def _validate_response(self, response: dict | None, status: int) -> None:
        """Response validation"""
        if status != 200:
            raise exceptions.ExternalServiceCommonError(f"Remote service responded status: {status}")
        if not response:
            raise exceptions.ExternalServiceCommonError("Invalid response")
        if msg := response.get("message"):
            raise exceptions.ExternalServiceCommonError(f"Remote service responded message: {msg}")

    def _as_tuple(self, data: dict, index: str) -> tuple:
        """Returns dict as a specify format tuple"""
        dates = tuple(data.get("datetime"))
        indices = tuple(data.get(index))
        statuses = tuple(data.get("status")) if index in self._state_indices else 0
        return dates, indices, statuses


class GFZClient(CommonGFZClient, HTTPBackend, AbstractClient):
    """Client for GFZ Helmholtz Centre for Geosciences Web Service API"""

    def get_nowcast(self,
                    start_time: str,
                    end_time: str,
                    index: str,
                    data_state: str = "all") -> dict | None:
        """Get geomagnetic three-hourly Kp index for period from GFZ sources:
            https://kp.gfz-potsdam.de/
            https://kp.gfz-potsdam.de/hp30-hp60
        Args:
            start_time: start UCS time. String in ISO-format, 'Z' as a timezone also possible
            end_time: start UCS time. String in ISO-format, 'Z' as a timezone also possible
            index: name of Kp index. possible values:
                'Kp', 'ap', 'Ap', 'Cp', 'C9', 'Hp30', 'Hp60', 'ap30', 'ap60', 'SN', 'Fobs', 'Fadj'
            data_state: string parameter 'status' for index. possible values: 'all', 'def'
        Raises:
            ExternalServiceCommonError: Error if response has not 'Ok' HTTP-status
        Returns:
            Response as a dict.
        """
        params = self._get_params(start_time, end_time, index, data_state)
        response, status = self._execute_request(method="GET", url=self._nowcast_link, params=params)
        self._validate_response(response, status)
        return response

    def get_forecast(self, index: str) -> dict:
        """Get geomagnetic index forecast from GFZ sources:
            https://spaceweather.gfz.de/products-data/forecasts/forecast-kp-index
            https://spaceweather.gfz.de/products-data/forecasts/forecast-hp30-hp60-indices
        Args:
            index: name of Kp index. valid values: 'Kp', 'Hp30', 'Hp60'
        Raises:
            ExternalServiceCommonError: Error if response has not 'Ok' HTTP-status
            InternalServiceError: Error if index not valid
        Returns:
            Dict, contains index forecast data
        """
        utils.check_index_name(index, is_forecast=True)
        response, status = self._execute_request(method="GET", url=self._get_forecast_url(index))
        self._validate_response(response, status)
        return response

    def get_kp_index(self,
                     starttime: str,
                     endtime: str,
                     index: str,
                     status: str = "all") -> tuple[tuple[str] | int, tuple[int] | int, tuple[str] | int]:
        """Get geomagnetic three-hourly Kp index for period
        Args:
            starttime: start UCS time
            endtime: start UCS time
            index: name of Kp index
            status: optional string parameter 'status' for index
        Returns:
            Tuple with dates, Kp index values, index statuses
        """
        try:
            data = self.get_nowcast(starttime, endtime, index, data_state=status)
        except (exceptions.ExternalServiceNetworkError,
                exceptions.ExternalServiceCommonError,
                exceptions.InternalServiceError) as exc:
            logger.error(str(exc), exc_info=logger.level == logging.DEBUG)
            return 0, 0, 0
        else:
            if not data:
                logger.warning(f"Remote service respond: {data}")
                return 0, 0, 0
            return self._as_tuple(data, index)


class GFZAsyncClient(CommonGFZClient, HTTPAsyncBackend, AbstractAsyncClient):
    """Async client for GFZ Helmholtz Centre for Geosciences  Web Service API"""

    async def get_nowcast(self,
                          start_time: str,
                          end_time: str,
                          index: str,
                          data_state: str = "all") -> dict:
        """Get geomagnetic three-hourly Kp index for period from GFZ sources:
            https://kp.gfz-potsdam.de/
            https://kp.gfz-potsdam.de/hp30-hp60
        Args:
            start_time: start UCS time. String in ISO-format, 'Z' as a timezone also possible
            end_time: start UCS time. String in ISO-format, 'Z' as a timezone also possible
            index: name of Kp index. possible values:
                'Kp', 'ap', 'Ap', 'Cp', 'C9', 'Hp30', 'Hp60', 'ap30', 'ap60', 'SN', 'Fobs', 'Fadj'
            data_state: string parameter 'status' for index. possible values: 'all', 'def'
        Raises:
            ExternalServiceCommonError: Error if response has not 'Ok' HTTP-status
        Returns:
            Dict, contains Kp index data for period
        """
        params = self._get_params(start_time, end_time, index, data_state)
        response, status = await self._make_request(method="GET", url=self._nowcast_link, params=params)
        self._validate_response(response, status)
        return response

    async def get_forecast(self, index: str) -> dict:
        """Get geomagnetic index forecast from GFZ sources:
            https://spaceweather.gfz.de/products-data/forecasts/forecast-kp-index
            https://spaceweather.gfz.de/products-data/forecasts/forecast-hp30-hp60-indices
        Args:
            index: name of Kp index. valid values: 'Kp', 'Hp30', 'Hp60'
        Raises:
            ExternalServiceCommonError: Error if response has not 'Ok' HTTP-status
            InternalServiceError: Error if index not valid
        Returns:
            Dict, contains index forecast data
        """
        utils.check_index_name(index, is_forecast=True)
        response, status = await self._make_request(method="GET", url=self._get_forecast_url(index))
        self._validate_response(response, status)
        return response

    async def get_kp_index(self,
                           starttime: str,
                           endtime: str,
                           index: str,
                           status: str = "all") -> tuple[tuple[str] | int, tuple[int] | int, tuple[str] | int]:
        """Get geomagnetic three-hourly Kp index for period as a tuple.
        Method implements getKpindex method from official python gfz_client (https://kp.gfz-potsdam.de/en/data)
        with same behaviour and added for compatibility purposes
        Args:
            starttime: start UCS time. String in ISO-format, 'Z' as a timezone also possible
            endtime: start UCS time. String in ISO-format, 'Z' as a timezone also possible
            index: name of Kp index. possible values:
                'Kp', 'ap', 'Ap', 'Cp', 'C9', 'Hp30', 'Hp60', 'ap30', 'ap60', 'SN', 'Fobs', 'Fadj'
            status: optional string parameter 'status' for index. possible values: 'all', 'def'
        Returns:
            Tuple with dates, Kp index values, index statuses
        """
        try:
            data = await self.get_nowcast(starttime, endtime, index, data_state=status)
        except (exceptions.ExternalServiceNetworkError,
                exceptions.ExternalServiceCommonError,
                exceptions.InternalServiceError) as exc:
            logger.error(str(exc), exc_info=logger.level == logging.DEBUG)
            return 0, 0, 0
        else:
            if not data:
                logger.warning(f"Remote service respond: {data}")
                return 0, 0, 0
            return self._as_tuple(data, index)
