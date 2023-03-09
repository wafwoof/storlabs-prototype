from datetime import datetime, timezone, timedelta

# Get the current time in UTC
offset = 0
now_utc = datetime.now(timezone.utc) + timedelta(hours=offset)
print("UTC:", now_utc)