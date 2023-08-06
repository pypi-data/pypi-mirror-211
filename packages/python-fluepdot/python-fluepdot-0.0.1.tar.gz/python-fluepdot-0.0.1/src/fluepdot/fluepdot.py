# python fluepdot module

import requests
import binascii
from requests import Response
from enum import Enum
from typing import Any, Dict, Optional, List

"""
  Small library to interact with a fluepdot controlled display
  https://fluepdot.readthedocs.io/en/latest/

  it should only be required to change the baseURL

  Currently there is no support for changing the timings.
"""

GetParam = Dict[str, Any]
PostParam = str


class Mode(Enum):
    FULL = 0
    DIFFERENTIAL = 1


# endpoints:
baseURL: str = None
frameURL: str = "/framebuffer"
pixelURL: str = "/pixel"
textURL: str = "/framebuffer/text"
fontURL: str = "/fonts"
modeURL: str = "/rendering/mode"

# size defaults:
width: int = 115
height: int = 16

fonts: Optional[List[str]] = None


def set_url(url: str):
    global baseURL
    baseURL = url


def post_time() -> None:
    import datetime
    dt: str = ""
    while True:
        ndt: str = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
        if ndt != dt:
            dt = ndt
            post_text(dt, x=8, y=1, font="fixed_7x14")


def get_size() -> (int, int):
    global width, height
    frame = get_frame()
    width = len(frame[0])
    height = len(frame) - 1
    return [width, height]


def get_frame() -> List[str]:
    r = _get(frameURL)
    return r.text.split('\n')


def get_pixel(x: int = 0, y: int = 0) -> bool:
    r = _get(pixelURL, get={x, y})
    print(r)
    return False


def get_fonts() -> None:
    r = _get(fontURL)
    fonts = r.text.split("\n")
    print(fonts)


def get_mode() -> Mode:
    r = _get(modeURL)
    return Mode(r.text)


def post_text(text: str, x: int = 0, y: int = 0, font: str = "DejaVuSans12") -> Response:
    return _post(textURL, get={"x": x, "y": y, "font": font}, post=text)


def post_frame_raw(frame: str) -> Response:
    return _post(frameURL, post=frame)


def post_frame(frame: List[List[bool]]) -> Response:
    data: List[List[str]] = [[" "] * width for _ in range(height)]
    for x, l in frame:
        for y, b in l:
            if b:
                try:
                    data[x, y] = "X"
                except IndexError as e:
                    print(e)
    return _post(frameURL, post=data)


def set_pixel(x: int = 0, y: int = 0) -> Response:
    return _post(pixelURL, get={x, y})


def unset_pixel(x: int = 0, y: int = 0) -> Response:
    return _delete(pixelURL, get={x, y})


def set_mode(mode: Mode = Mode.FULL) -> Response:
    return _put(modeURL, post=str(mode.value))


def _delete(endpoint: str, get: GetParam = {}, post: PostParam = '') -> Response:
    if baseURL == None:
        raise RuntimeError('baseURL is None, call set_url')
    return requests.delete(url=baseURL + endpoint, params=get)


def _post(endpoint: str, get: GetParam = {}, post: PostParam = '') -> Response:
    if baseURL == None:
        raise RuntimeError('baseURL is None, call set_url')
    return requests.post(url=baseURL + endpoint, params=get, data=post)


def _put(endpoint: str, get: GetParam = {}, post: PostParam = '') -> Response:
    if baseURL == None:
        raise RuntimeError('baseURL is None, call set_url')
    return requests.put(url=baseURL + endpoint, params=get, data=post)


def _get(endpoint: str, get: GetParam = {}) -> Response:
    if baseURL == None:
        raise RuntimeError('baseURL is None, call set_url')
    return requests.get(url=baseURL + endpoint, params=get)


if __name__ == "__main__":
    pass
