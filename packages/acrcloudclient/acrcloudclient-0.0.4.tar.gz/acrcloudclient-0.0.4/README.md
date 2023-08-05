# acrcloud
ACR Cloud Python Client

API ACRCloud Doc
---

https://docs.acrcloud.com/reference/console-api


ACRClient Examples Usage
---

List and remove audios that are created on 2021

```python
from acrcloud import ACRCloudClient
import os
ACR_TOKEN=os.getenv("ACR_TOKEN")

def log(bucket, msg):
    """Local log function"""
    print(f"B:{bucket.name} - {msg}")

acr = ACRCloudClient(ACR_TOKEN)
for bucket in acr.list_buckets(search="my-bucket-"):
    print("Processing bucket:", bucket.name)
    audios = bucket.list_audios(order="asc")
    for a in audios:
        if "2021" in a.created_at:
            a.delete()
            log(bucket, f"Delete audio: {a.id} - {a.created_at}")
        else:
            log(bucket, "Not found any audio from 2021")
            break
```

Environment Variables

ACR_CLOUD_TOKEN = <TOKEN>

### Roadmap plan

- [ ] Handle date fields with datetime object
- [X] Handle TOKEN through default environment variables  
- [X] Publish to pip