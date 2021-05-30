# backoff-circuitbreaker

This repo contains two method to handle polling of APIs
which gives irregular response intermittent failures

## Method
* Exponential Back off 
* Circuit Breaker -> ```python example/circuit_breaker.py```

### Why not Simple Retry?
Suppose the service we are calling is already overloaded or there is rate limiting implemented 
at the service end and it is giving transient faults then by doing simple retry after constant time 
there may be a case that our retry request are further adding load to the busy service and will take longer to recover.

## One Issue with Exponential Backoff
If the transient fault is long lasting then our service will keep on retrying till maximum retries for every new request we get, that will be wasting of our resources.

### The above issue solved by using circuit breaker
If the transient fault is long lasting then the circuit breaker is opened after the first request which goes to maximum retries, for any further request the circuit breaker directly sends an error message that the service is down(no retries).

After some timeout period circuit breaker will move to HALF-OPEN state.
In this state, it will allow a service call which will determine if the service has become available or not. If the service is not available it goes back to OPEN state. If the service becomes available after this timeout, the circuit breaker moves to CLOSED state. The callers will be able to call the service and the usual retry mechanism will come in play again.