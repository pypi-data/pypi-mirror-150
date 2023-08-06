import logging
from datetime import datetime, date, time
from json import dumps
from typing import List, Iterable, Optional, Union, Dict, Sequence

import requests
from requests import HTTPError


def serialize(obj):
    """JSON serializer that accepts datetime & date"""
    if isinstance(obj, date) and not isinstance(obj, datetime):
        obj = datetime.combine(obj, time.min)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, set):
        return sorted(obj)


class AmcatClient:
    def __init__(self, host, username, password, ignore_tz=True):
        self.host = host
        self.username = username
        self.token = self.get_token(password)
        self.ignore_tz = ignore_tz

    def get_token(self, password) -> str:
        r = requests.post(self.url("auth/token"), data=dict(username=self.username, password=password))
        r.raise_for_status()
        return r.json()["access_token"]

    def url(self, url=None, index=None):
        url_parts = [self.host] + (["index", index] if index else []) + ([url] if url else [])
        return "/".join(url_parts)

    def request(self, method, url=None, ignore_status=None, headers=None, **kargs):
        if headers is None:
            headers = {}
        headers['Authorization']= f"Bearer {self.token}"
        r = requests.request(method, url, headers=headers, **kargs)
        if not (ignore_status and r.status_code in ignore_status):
            try:
                r.raise_for_status()
            except HTTPError:
                if r.text:
                    logging.error(f"Response body: {r.text}")
                raise
        return r

    def get(self, url=None, index=None, params=None, ignore_status=None):
        return self.request("get", url=self.url(url, index), params=params, ignore_status=ignore_status)

    def post(self, url=None, index=None, json=None, ignore_status=None):
        if json:
            data = dumps(json, default=serialize)
            headers = {'Content-Type': 'application/json'}
        else:
            data = None
            headers = {}

        return self.request("post", url=self.url(url, index), data=data, headers=headers, ignore_status=ignore_status)

    def put(self, url=None, index=None, json=None, ignore_status=None):
        return self.request("put", url=self.url(url, index), json=json, ignore_status=ignore_status)

    def delete(self, url=None, index=None, ignore_status=None):
        return self.request("delete", url=self.url(url, index), ignore_status=ignore_status)

    def list_indices(self) -> List[dict]:
        """
        List all indices on this server
        :return: a list of index dicts with keys name and (your) role
        """
        return self.get("index/").json()

    def documents(self, index: str, q: Optional[str]= None, *,
                  fields=('date', 'title', 'url'), scroll='2m', per_page=100, **params) -> Iterable[dict]:
        """
        Perform a query on this server, scrolling over the results to get all hits

        :param index: The name of the index
        :param q: An optional query
        :param fields: A list of fields to retrieve (use None for all fields, '_id' for id only)
        :param scroll: type to keep scroll cursor alive
        :param per_page: Number of results per page
        :param params: Any other parameters passed as query arguments
        :return: an iterator over the found documents with the requested (or all) fields
        """
        params['scroll'] = scroll
        params['per_page'] = per_page
        if fields:
            params['fields'] = ",".join(fields)
        if q:
            params['q'] = q
        while True:
            r = self.get("documents", index=index, params=params, ignore_status=[404])
            if r.status_code == 404:
                break
            d = r.json()
            yield from d['results']
            params['scroll_id'] = d['meta']['scroll_id']

    def query(self, index: str, *,
              scroll='2m', per_page=100,
              sort: Union[str, dict, list] = None,
              fields: Sequence[str] = ('date', 'title', 'url'),
              queries: Union[str, list, dict] = None,
              filters: Dict[str, Union[str, list, dict]] = None,
              date_fields: Sequence[str] = ('date',)):
        body = dict(filters=filters, queries=queries, fields=fields, sort=sort,
                scroll=scroll, per_page=per_page)
        body = {k: v for (k, v) in body.items() if v is not None}
        while True:
            r = self.post("query", index=index, json=body, ignore_status=[404])
            if r.status_code == 404:
                break
            d = r.json()
            for res in d['results']:
                for date_field in date_fields:
                    if res.get(date_field):
                        date = res[date_field][:10] if self.ignore_tz else res[date_field]
                        res[date_field] = datetime.fromisoformat(date)
                yield res
            body['scroll_id'] = d['meta']['scroll_id']

    def create_index(self, index: str, guest_role: Optional[str] = None):
        body = {"name": index}
        if guest_role:
            body['guest_role'] = guest_role
        return self.post("index/", json=body).json()

    def check_index(self, index: str) -> Optional[dict]:
        r = self.get(index=index, ignore_status=[404])
        if r.status_code == 404:
            return None
        return r.json()

    def delete_index(self, index: str) -> bool:
        r = self.delete(index=index, ignore_status=[404])
        return r.status_code != 404

    def upload_documents(self, index: str, articles: Iterable[dict], columns: dict = None):
        body = {"documents": articles}
        if columns:
            body['columns'] = columns
        return self.post("documents", index=index, json=body)

    def update_document(self, index: str, doc_id, body):
        self.put(f"documents/{doc_id}", index, json=body)

    def get_document(self, index: str, doc_id):
        return self.get(f"documents/{doc_id}", index).json()

    def delete_document(self, index: str, doc_id):
        self.delete(f"documents/{doc_id}", index)

    def set_fields(self, index: str, body):
        self.post("fields", index, json=body)

    def get_fields(self, index: str):
        return self.get("fields", index).json()
