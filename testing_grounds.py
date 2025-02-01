from datetime import datetime, timezone
import time
from itsdangerous import TimedSerializer, URLSafeTimedSerializer
# print(datetime.now(timezone.utc))

# print(datetime.utcnow)
#
# with open("bungee_gum/static/profile-pics/default.jpg") as f:
#     print(f.name)
s = TimedSerializer('secret', "30")
token = s.dumps({'user_id': 1})
time.sleep(6)
s.loads(token, max_age=5)


