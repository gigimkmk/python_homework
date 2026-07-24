import threading

def is_prime(number):
    if number < 2:
        print(f"{number} -> Not Prime")
        return

    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            print(f"{number} -> Not Prime")
            return

    print(f"{number} -> Prime")


num_list = [17, 25, 74, 199, 101, 41, 39, 50, 20, 19, 51]

threads = []

for number in num_list:
    thread = threading.Thread(target=is_prime, args=(number,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()