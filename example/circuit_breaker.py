import pybreaker
import mock_server
import datetime
import requests
import time, math

FAILURES = 2
TIMEOUT = 6

circuit_breaker = pybreaker.CircuitBreaker(fail_max=FAILURES, reset_timeout=TIMEOUT)

@circuit_breaker
def get_resource(url, port):
    response = requests.get("http://{}:{}/".format(url, port))
    return response.text


def test(iterations=10, delay=1, url="localhost", port=5000):
    for i in range(iterations):
        try:
            get_resource(url, port)
        except:
            pass
        print_circuit_state()
        time.sleep(delay)


def print_circuit_state():
    state = circuit_breaker._state_storage.state
    time_left = TIMEOUT
    if circuit_breaker._state_storage.opened_at:
        elapse_time = datetime.datetime.utcnow() - circuit_breaker._state_storage.opened_at
        time_left = math.floor(TIMEOUT - elapse_time.total_seconds())
    print("circuit state: {}. Time till open: {}".format(state, time_left))


if __name__ == "__main__":
    print("Server is turned OFF...")
    test()

    print("Server is turning ON...")
    with mock_server.app.run("localhost", 5000):
        test()
