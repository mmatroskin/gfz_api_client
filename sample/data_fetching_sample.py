import asyncio
import time

from gfz_client import GFZClient, GFZAsyncClient, exceptions
from gfz_client.types import IndexType


START = "2024-07-15T00:00:00Z"
END = "2025-01-14T23:59:59Z"


def main():
    print("Classic client")
    total_start_time = time.time()
    client = GFZClient()
    start_time = time.time()
    test_result_0_kp = client.get_forecast(IndexType.Kp.value)
    test_result_0_hp3 = client.get_forecast(IndexType.Hp30.value)
    test_result_0_hp6 = client.get_forecast(IndexType.Hp60.value)
    try:
        test_result_1_kp = client.get_nowcast(START, END, IndexType.Kp.value)
    except exceptions.ExternalServiceCommonError as exc:
        test_result_1_kp = None
        print(str(exc))
    try:
        test_result_1_hp = client.get_nowcast(START, END, IndexType.Hp60.value)
    except exceptions.ExternalServiceCommonError as exc:
        test_result_1_hp = None
        print(str(exc))
    test_result_2_kp = client.get_kp_index(START, END, IndexType.Kp.value)
    test_result_2_hp = client.get_kp_index(START, END, IndexType.Hp60.value)
    end_time = time.time()
    result = test_results(test_result_0_kp, test_result_0_hp3, test_result_0_hp6, test_result_1_kp,
                          test_result_1_hp, test_result_2_kp, test_result_2_hp)
    duration = round((end_time - start_time), 3)
    result_duration = round((time.time() - total_start_time), 3)
    print(f"Result: {result}, Requests time: {duration}sec, Total time: {result_duration}sec")
    try:
        test_result_error = client.get_nowcast(START, END, "fake_index")
    except exceptions.InternalServiceError as exc:
        print("Error:", str(exc), sep=" ")
    print("Done", end="\n\n")


async def main_async():
    print("Async client")
    total_start_time = time.time()
    client = GFZAsyncClient()
    start_time = time.time()
    test_result_0_kp, test_result_0_hp3, test_result_0_hp6, test_result_1_kp, test_result_1_hp, test_result_2_kp, \
        test_result_2_hp = await asyncio.gather(
            *[
                client.get_forecast(IndexType.Kp.value),
                client.get_forecast(IndexType.Hp30.value),
                client.get_forecast(IndexType.Hp60.value),
                client.get_nowcast(START, END, IndexType.Kp.value),
                client.get_nowcast(START, END, IndexType.Hp60.value),
                client.get_kp_index(START, END, IndexType.Kp.value),
                client.get_kp_index(START, END, IndexType.Hp60.value)
            ],
            return_exceptions=True
        )
    end_time = time.time()
    if isinstance(test_result_1_kp, Exception):
        print(repr(test_result_1_kp))
        test_result_1_kp = None
    if isinstance(test_result_1_hp, Exception):
        print(repr(test_result_1_hp))
        test_result_1_hp = None
    result = test_results(test_result_0_kp, test_result_0_hp3, test_result_0_hp6, test_result_1_kp,
                          test_result_1_hp, test_result_2_kp, test_result_2_hp)
    duration = round((end_time - start_time), 3)
    result_duration = round((time.time() - total_start_time), 3)
    print(f"Result: {result}, Requests time: {duration}sec, Total time: {result_duration}sec")
    test_result_error = await client.get_kp_index(START, END, "fake_index")
    print("Error Result:", test_result_error, sep=" ")
    print("Done", end="\n")


def test_results(test_result_0_kp,
                 test_result_0_hp3,
                 test_result_0_hp6,
                 test_result_1_kp,
                 test_result_1_hp,
                 test_result_2_kp,
                 test_result_2_hp):
    return bool(test_result_0_kp) \
        and bool(test_result_0_hp3) \
        and bool(test_result_0_hp6) \
        and bool(test_result_1_kp) \
        and bool(test_result_1_hp) \
        and test_result_2_kp != (0, 0, 0) \
        and test_result_2_hp != (0, 0, 0) \
        and test_result_1_kp.get("meta") is not None \
        and test_result_1_hp.get("meta") is not None


if __name__ == '__main__':
    print("\n")
    main()
    asyncio.run(main_async())
