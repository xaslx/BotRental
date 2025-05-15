```
ab -k -c 5 -n 20000 'http://localhost:8000/' & \
ab -k -c 5 -n 2000 'http://localhost:8000/status/400' & \
ab -k -c 5 -n 3000 'http://localhost:8000/status/409' & \
ab -k -c 5 -n 5000 'http://localhost:8000/status/500' & \
ab -k -c 50 -n 5000 'http://localhost:8000/status/200?seconds_sleep=1' & \
ab -k -c 50 -n 2000 'http://localhost:8000/status/200?seconds_sleep=2'
```