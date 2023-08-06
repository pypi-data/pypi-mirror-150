'''
Datafi access.

Copyright (c) 2022, Datafi Labs Inc. All Rights Reserved.
'''

from http import client
from urllib import parse
import json
import torch
from torch.utils.data import Dataset
from typing import Any, Callable, Dict, Iterable, Union

_url = "https://es3ft59m1l.execute-api.us-west-2.amazonaws.com/datafi"

class _Dataset(Dataset):

  def __init__(self, data: torch.Tensor, scale: Callable[[torch.Tensor], torch.Tensor]):
    self._data = data
    self.scale = scale
  
  def __len__(self) -> int:
    return len(self._data)

  def __getitem__(self, index: int) -> Any:
    return self._data[index]

class Datafi:
  def __init__(self, url: str = _url):
    self._url = parse.urlparse(url)
    self._dataset_info: Dict[str, Dict[str, str]] = {}

  def login(self, email: str, password: str) -> bool:
    conn = client.HTTPSConnection(self._url.netloc)
    conn.request("POST", self._url.path + "/login", body=json.dumps({
      "username": email,
      "password": password
    }))
    http_resp = conn.getresponse()
    if http_resp.status != 200:
      return False
    resp = json.loads(http_resp.read())
    for k, v in resp["datasets"].items():
      if "endpoint" not in v:
        continue
      self._dataset_info[v["name"]] = {
        "id": k,
        "endpoint": v["endpoint"],
        "token": v["connectorToken"]
      }
    return True
  
  '''
  Dataset using DQL connection to edge server.
  '''
  def dataset(
    self,
    name: str,
    record: str,
    fields: Iterable[str],
    total_size: int = 100000,
    fetch_size: int = 1000,
    convert: Callable[[Dict], Union[Iterable, None]] = None
  ) -> Dataset:
    if name not in self._dataset_info:
      raise ValueError(f"{name}: no such dataset")
    dataset_info = self._dataset_info[name]
    url = parse.urlparse(dataset_info["endpoint"])
    conn = client.HTTPSConnection(url.netloc)
    headers = {
      "Connector-Token": dataset_info["token"],
    }

    query = "USE {};".format(dataset_info["id"])
    query += " SELECT {} FROM {}".format(', '.join(fields), record)
    query += " LIMIT {}".format(fetch_size)
    query += " OFFSET {}"
    data_values = []
    print("Loading", end="", flush=True)
    for offset in range(0, total_size, fetch_size):
      print(".", end="", flush=True)
      body = {"query": query.format(offset)}
      conn.request("POST", url.path + "/dataview", body=json.dumps(body), headers=headers)
      resp: Dict[str, Any] = json.loads(conn.getresponse().read())
      if "data" not in resp:
        raise IOError(resp)
      for _, d in enumerate(resp["data"]):
        d_val = d if convert is None else convert(d)
        if d_val is None:
          continue
        data_values.append(d_val)
    data = torch.tensor(data_values)
    self._mean = torch.mean(data, dim=0)
    self._std = torch.std(data, dim=0)
    self._data = (data - self._mean) / self._std
    print("done")

    def scale(v: torch.Tensor) -> torch.Tensor:
      '''
      Scale x/y following the normalization.
      '''
      if v.shape[-1] == 1:
        return v * self._std[-1] + self._mean[-1]
      return (v - self._mean[:-1]) / self._std[:-1]

    return _Dataset(self._data, scale)
  