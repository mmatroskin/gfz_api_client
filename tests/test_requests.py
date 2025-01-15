import asyncio
import time

from gfz_client import GFZClient, GFZAsyncClient
from gfz_client.types import IndexType


START = "2024-07-15T00:00:00Z"
END = "2025-01-14T23:59:59Z"


def main():
    total_start_time = time.time()
    client = GFZClient()
    start_time = time.time()
    test_result_0_kp = client.get_forecast(IndexType.Kp.value)
    test_result_0_hp3 = client.get_forecast(IndexType.Hp30.value)
    test_result_0_hp6 = client.get_forecast(IndexType.Hp60.value)
    test_result_1_kp = client.get_nowcast(START, END, IndexType.Kp.value)
    test_result_1_hp = client.get_nowcast(START, END, IndexType.Hp60.value)
    test_result_2_kp = client.get_kp_index(START, END, IndexType.Kp.value)
    test_result_2_hp = client.get_kp_index(START, END, IndexType.Hp60.value)
    end_time = time.time()
    duration = round((end_time - start_time), 3)
    result = test_results(test_result_0_kp, test_result_0_hp3, test_result_0_hp6, test_result_1_kp,
        test_result_1_hp, test_result_2_kp, test_result_2_hp)
    result_duration = round((time.time() - total_start_time), 3)
    print(f"Classic: {result}, Requests time: {duration}sec, Total time: {result_duration}sec")


async def main_async():
    total_start_time = time.time()
    client = GFZAsyncClient()
    start_time = time.time()
    test_result_0_kp = await client.get_forecast(IndexType.Kp.value)
    test_result_0_hp3 = await client.get_forecast(IndexType.Hp30.value)
    test_result_0_hp6 = await client.get_forecast(IndexType.Hp60.value)
    test_result_1_kp = await client.get_nowcast(START, END, IndexType.Kp.value)
    test_result_1_hp = await client.get_nowcast(START, END, IndexType.Hp60.value)
    test_result_2_kp = await client.get_kp_index(START, END, IndexType.Kp.value)
    test_result_2_hp = await client.get_kp_index(START, END, IndexType.Hp60.value)
    end_time = time.time()
    duration = round((end_time - start_time), 3)
    result = test_results(test_result_0_kp, test_result_0_hp3, test_result_0_hp6, test_result_1_kp,
        test_result_1_hp, test_result_2_kp, test_result_2_hp)
    result_duration = round((time.time() - total_start_time), 3)
    print(f"Async: {result}, Requests time: {duration}sec, Total time: {result_duration}sec")


def test_results(test_result_0_kp,
                 test_result_0_hp3,
                 test_result_0_hp6,
                 test_result_1_kp,
                 test_result_1_hp,
                 test_result_2_kp,
                 test_result_2_hp):
    return bool(test_result_0_kp)\
        and bool(test_result_0_hp3)\
        and bool(test_result_0_hp6)\
        and bool(test_result_1_kp)\
        and bool(test_result_1_hp)\
        and test_result_2_kp != (0, 0, 0)\
        and test_result_2_hp != (0, 0, 0)\
        and test_result_1_kp.get("meta") is not None\
        and test_result_1_hp.get("meta") is not None


if __name__ == '__main__':
    main()
    asyncio.run(main_async())
