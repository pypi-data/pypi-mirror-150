The client library of Kylin Autosolve
=

_by Kylin Inc._

This is a client library of Kylin Autosolve based on the WebSocket protocol.

Installation
==
```
pip install kylin-autosolve-client-python
```

Usage
==

Initialize a client
===

```python
import kylinautosolve

client = kylinautosolve.KylinAutosolveClient()
```

Connect to the autosolve service
===
```python
cliennt.access_token = 'ACCESS_TOKEN'
client.cient_key = 'CLIENT_KEY'
client.start()
```

Add a listener to receive result
===
```python
def handler(evt):
  notification = evt.notification
  task_result = notification.task_result()
  evt.handled += 1

  print('received task result:', task_result)

client.on('notification:task_result', handler)
```
**NOTE**
The `token` field is encoded in JSON format.


Create a task to solve a challenge
===
```python
  options = {
    'site_key': '6Lfv-q0ZAAAAADy0U9JUaCPCZI15U-7jhbAiYa0U',
    'version': '3',
    'action': 'login'
  }
  message = client.make_create_task_message({
    'google',
    'https://recaptcha-test.kylinbot.io/',
    options.get('timeout', 0'),
    options
  })

  await client.when_ready()
  response = await client.invoke(message)
  print('response:', response)
```

Poll the result of a task
===
You don't have to poll the result usually, the autosolve server will notify client when it got the result from **Kylin One Click**, install a notification handler to receive result instead.
```python
await client.invoke(client.make_get_task_result_message(
    kylinautosolve.GetTaskResultRequest(
        task_id=create_task_response.create_task.task_id
    )))
```

Cancel a request
===
```python
await client.invoke(client.make_cancel_task_message(
    kylinautosolve.CancelTaskRequest(
        task_id=create_task_response.create_task.task_id
    )))
```

Cancel all requests
===
```python
await client.invoke(client.make_cancel_task_message())
```
