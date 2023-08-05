from requests import Session
from typing import List, Optional
from dataclasses import dataclass, field
import json
from pathlib import Path
import os

ACR_API = "https://api-v2.acrcloud.com"

TOKEN = os.getenv("ACR_CLOUD_TOKEN", "")
# DEFAULT_LABELS = ["tmp", "audio", "recognizer"]

class APIException(Exception):
    """ACRCloud API Exception"""
    def __init__(self, response, message) -> None:
        self.message = f"Error in ACRCloud API - {message}"
        self.message = response.text
        super().__init__(self.message)


@dataclass
class ACRAudio:
    """ACRCloud Audio object"""
    title: str
    user_defined: dict
    session: "ACRCloudClient"
    id: Optional[int] = None
    uid: Optional[int] = None
    bucket_id: Optional[int] = None
    data_type: Optional[str] = None
    acr_id: Optional[str] = None
    state: Optional[int] = None
    duration: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    audio_id: Optional[str] = None
    error: Optional[str] = None

    def delete(self):
        sub_path = f"/api/buckets/{self.bucket_id}/files/{self.id}"
        return self.session.delete(ACR_API + sub_path).text

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


@dataclass
class ACRBucket:
    """ACRCloud Bucket object"""
    id: int
    session: "ACRCloudClient"
    uid: Optional[int] = None
    name: Optional[str] = ""
    type: Optional[str] = ""
    state: Optional[str] = ""
    region: Optional[str] = None
    metadata_template: Optional[str] = None
    labels: list[str] = field(default_factory=list)
    net_type: Optional[int] = None
    tracker: Optional[str] = ""
    created_at: Optional[str] = ""
    updated_at: Optional[str] = ""
    num: Optional[int] = None
    size: Optional[str] = None
    access_permission: Optional[str] = None

    def upload_audio(self, file_path, user_defined={}) -> ACRAudio:
        """Upload an audio file to the bucket"""
        sub_path = f"/api/buckets/{self.id}/files"

        print(f"Trying to upload {file_path}")
        path = Path(file_path)
        name = path.name
        title = name.replace(path.suffix, "")
        payload = {
            "title": title,
            "audio_id": title,
            "data_type": "audio",
            "user_defined": json.dumps(user_defined),
        }
        with open(file_path, "rb") as f:
            res = self.session.post(ACR_API + sub_path, data=payload, files={"file": f})
        if not res.ok:
            raise APIException(res, f"Error uploading audio {title}")
        return ACRAudio(session=self.session, **res.json()["data"])

    def list_audios(self, page=1, order="desc") -> "PaginatedResponse":
        """List all audios in the bucket"""
        return self.session.list_audios(self.id, page, "created_at", order)

    def clear(self) -> None:
        """Delete all audios in the bucket"""
        audios = self.list_audios()
        sub_path = f"/api/buckets/{self.id}/files/"
        joined_ids = ",".join(map(lambda x: str(x.id), audios))
        self.session.delete(ACR_API + sub_path + joined_ids)


class PaginatedResponse:
    """Handle paginated responses from ACRCloud API"""
    def __init__(self, session, response, serializer, params=""):
        self.session = session
        self.items = response["data"]
        self.serializer = serializer
        self.params = params
        if "links" in response:
            self.links = response["links"]
        if "meta" in response:
            self.meta = response["meta"]

    def has(self, direction):
        """Check if the response has a next or previous page"""
        return direction in self.links and bool(self.links[direction])

    def prepare_response(self, res):
        """Wrap the response in a PaginatedResponse object"""
        return PaginatedResponse(self.session, res.json(), self.serializer, self.params)

    def next(self):
        """Follow the next page link"""
        return self.handle_direction("next")

    def prev(self):
        """Follow the previous page link"""
        return self.handle_direction("prev")

    def handle_direction(self, direction):
        """Generic method to follow a link in a direction"""
        if direction not in ["next", "prev"]:
            raise ValueError("Direction must be either 'next' or 'prev'")
        if not self.has(direction):
            return None
        res = self.session.get(self.links[direction] + self.params)
        return self.prepare_response(res)

    # Inspired by stripe-python
    # https://github.com/stripe/stripe-python/blob/fa26fa57ff980eee12ab6b770df601e6dd7bef34/stripe/api_resources/list_object.py#L80
    def __iter__(self):
        """Iterate over all items in the paginated response and yield the serializer"""
        page = self

        while True:
            for item in page.items:
                yield self.serializer(session=self.session, **item)

            page = page.next()

            if not page or page.is_empty:
                break

    @property
    def is_empty(self):
        """Check if the response is empty"""
        return not self.items

    def __repr__(self):
        return f"<PaginatedResponse: Page {self.meta['current_page']} of {self.meta['last_page']}>"

    def __str__(self):
        return f"<PaginatedResponse: Page {self.meta['current_page']} of {self.meta['last_page']}>"


class ACRCloudClient(Session):
    """Main ACRCloud API client"""
    def __init__(self, *args, token=TOKEN, **kwargs):
        """Constructor for ACRCloudClient"""
        super().__init__(*args, **kwargs)
        if not token:
            raise ValueError("Token is required")
        self.token = token
        self.headers.update({"Authorization": f"Bearer {self.token}"})

    def create_bucket(
        self,
        bucket_name,
        labels=None,
        region="ap-southeast-1",
    ):
        """Create a new bucket"""
        if not labels:
            labels = []
        data = {
            "name": bucket_name,
            "type": "File",
            "labels": labels,
            "net_type": 1,
            "region": region,
        }
        res = self.post(ACR_API + "/api/buckets", json=data)
        print(res.text)
        return res

    def list_buckets(self, region="us-west-2", search="") -> list[ACRBucket]:
        """List all buckets in the account"""
        sub_path = f"/api/buckets?region={region}&search={search}"
        res = self.get(ACR_API + sub_path)
        return PaginatedResponse(self, res.json(), ACRBucket)

    def get_bucket_by_name(self, name):
        """Low performance method to get a bucket by name"""
        buckets = self.list_buckets()
        for bucket in buckets:
            if bucket.name == name:
                return bucket

    def get_bucket(self, bucket_id) -> ACRBucket:
        """Get Bucket by ID"""
        # sub_path = f"/api/buckets/{bucket_id}"
        return ACRBucket(session=self, id=bucket_id)

    # Audio Actiones

    def list_audios(
        self, bucket_id, page=1, sort="created_at", order="desc"
    ) -> PaginatedResponse:
        """List audio files in a bucket"""
        params = f"&sort={sort}&order={order}"
        sub_path = f"/api/buckets/{bucket_id}/files?page={page}{params}"
        res = self.get(ACR_API + sub_path)
        if res.ok:
            res = self.get(ACR_API + sub_path).json()
        else:
            print(res.text)
            raise APIException(res, "Error listing audios")
        return PaginatedResponse(self, res, ACRAudio, params=params)

    def create_audio(
        self: Session, title: str, audio_id: str, data_type: str, user_defined: dict
    ):
        """Create a new audio file in a bucket"""
        return ACRAudio(
            session=self,
            title=title,
            audio_id=audio_id,
            data_type=data_type,
            user_defined=user_defined,
        )

    def delete_audio(self, bucket_id, audio_id):
        """Delete an audio file from a bucket"""
        sub_path = f"/api/buckets/{bucket_id}/files/{audio_id}"
        return self.delete(ACR_API + sub_path).text

    def upload_audio(self, bucket_id, file_path, title, audio_id, user_defined=None, data_type="audio"):
        """Upload an audio file to a bucket"""
        sub_path = f"/api/buckets/{bucket_id}/files"
        if not user_defined:
            user_defined = {}
        payload = {
            "title": title,
            "audio_id": audio_id,
            "data_type": data_type,
            "user_defined": json.dumps(user_defined),
        }
        with open(file_path, "rb", encoding="utf8") as file:
            res = self.post(ACR_API + sub_path, data=payload, files={"file": file})
        return ACRAudio(session=self, **res.json()["data"])
