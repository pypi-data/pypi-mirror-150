import json
import os
from pydoc import cli
import sys
import asyncio
import datetime

SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(SCRIPT_DIR)

import kylinautosolve

CLIENT_KEY = 'w8mp5inwszowft3kyc'

async def main(token: str) -> None:
    if not token:
        print('The acccess token is required.')
        return

    client = kylinautosolve.KylinAutosolveClient()
    client.client_key = CLIENT_KEY
    client.access_token = token

    try:
        client.start()
        await client.when_ready()

        options = {
        'info': {
            'id': 'TASK_ID',
            'timestamp': int(datetime.datetime.now().timestamp() * 1000),
            'inputName': 'code',
            'inputLabel': 'Enter the code sent to XXXX'
        },
        'type': 'sms-code',
        'actionUrl': 'https://wwww.yeezysupply.com/callback/smscode',
        'method': 'GET',
        'callbackUrlPattern': 'https://wwww.yeezysupply.com/callback/'
        }
        create_task_response = await client.invoke(
            client.make_create_task_message(
                kylinautosolve.CreateTaskRequest(
                'yeezysupply-3ds',
                'https://www.yeezysupply.com/payment',
                options.get('timeout', None),
                options)))
        print(create_task_response)

        for i in range(100):
            poll_response = await client.invoke(
                client.make_get_task_result_message(
                    kylinautosolve.GetTaskResultRequest(
                        create_task_response.create_task.task_id
                )))
            if poll_response.get_task_result and poll_response.get_task_result.token:
                print(poll_response)
                break
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        client.stop()

asyncio.get_event_loop().run_until_complete(main(len(sys.argv) > 1 and sys.argv[1] or ''))
