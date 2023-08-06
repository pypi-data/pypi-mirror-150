import json
import os
import sys
import asyncio

SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(SCRIPT_DIR)

import kylinautosolve

CLIENT_KEY = 'w8mp5inwszowft3kyc'

async def main(token: str) -> None:
    if not token:
        print('The acccess token is required.')
        return

    service = kylinautosolve.KylinAutosolveService(CLIENT_KEY)
    service.start(token)

    try:
        options = {
            'site_key': '6Lfv-q0ZAAAAADy0U9JUaCPCZI15U-7jhbAiYa0U',
            'version': '3',
            'action': 'login',
        }
        result = await service.solve(
            kylinautosolve.CreateTaskRequest(
                'google',
                'https://recaptcha-test.kylinbot.io/',
                options.get('timeout', None),
                options))
        print(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        service.stop()

asyncio.get_event_loop().run_until_complete(main(len(sys.argv) > 1 and sys.argv[1] or ''))
