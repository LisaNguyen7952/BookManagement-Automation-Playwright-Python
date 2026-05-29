import time


def wait_for_table_update_and_ready(row_locator, timeout=10000, interval=0.3):
    start = time.time()

    try:
        old_count = row_locator.count()
    except:
        old_count = -1

    while (time.time() - start) * 1000 < timeout:
        try:
            new_count = row_locator.count()

            # table có data là OK
            if new_count > 0:
                return

            # hoặc count thay đổi
            if new_count != old_count:
                return

        except:
            pass

        time.sleep(interval)

    raise TimeoutError("⏰ Table did not update")
def wait_for_table_stable(row_locator, timeout=10000):
    start = time.time()
    last_count = -1
    stable_round = 0

    while (time.time() - start) * 1000 < timeout:
        try:
            current_count = row_locator.count()

            if current_count == last_count:
                stable_round += 1
            else:
                stable_round = 0

            # ổn định 2-3 lần liên tiếp
            if stable_round >= 2:
                return

            last_count = current_count

        except:
            pass

        time.sleep(0.3)

    raise TimeoutError("⏰ Table not stable")