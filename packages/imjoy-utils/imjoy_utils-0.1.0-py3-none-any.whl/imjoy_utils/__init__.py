"""Implement imjoy-utils."""
"""Provide tests for imjoy-utils."""
import io
import locale
import os

try:
    from js import eval, location

    _sync_xhr_head = eval(
        """globalThis._sync_xhr_head = function(url){
        var request = new XMLHttpRequest();
        request.open('HEAD', url, false);  // `false` makes the request synchronous
        request.send(null);
        return request
    }
    """
    )

    _sync_xhr_get = eval(
        """globalThis._sync_xhr_get = function(url, start, end){
        var request = new XMLHttpRequest();
        request.open('GET', url, false);  // `false` makes the request synchronous
        if(typeof start === 'number' && typeof end === 'number' ){
            request.setRequestHeader("range", `bytes=${start||0}-${end||0}`)
        }
        request.responseType = "arraybuffer";
        request.send(null);
        return request
    }
    """
    )

    _sync_xhr_post = eval(
        """globalThis._sync_xhr_post = function(url, rawData, type, append){
        var request = new XMLHttpRequest();
        request.open('POST', url, false);  // `false` makes the request synchronous
        var formData = new FormData();
        var file = new Blob([new Uint8Array(rawData)],{type});
        formData.append("file", file);
        if(append) formData.append("append", "1");
        request.send(formData);
        return request
    }
    """
    )

    _sync_xhr_put = eval(
        """globalThis._sync_xhr_put = function(url, rawData, type, append){
        if(append) throw new Error("append is not supported for put requests");
        var request = new XMLHttpRequest();
        request.open('PUT', url, false);  // `false` makes the request synchronous
        var formData = new FormData();
        var file = new Blob([new Uint8Array(rawData)],{type});
        request.send(file);
        return request
    }
    """
    )
    IS_PYODIDE = True
except ImportError:
    from urllib.request import Request, urlopen

    IS_PYODIDE = False


class HTTPFile(io.IOBase):
    """A virtual file for reading content via HTTP."""

    def __init__(
        self,
        url,
        mode="r",
        encoding=None,
        newline=None,
        name=None,
        upload_method="POST",
    ):
        """Initialize the http file object."""
        self._url = url
        self._pos = 0
        self._size = None
        self._mode = mode
        self.name = name
        assert mode in ["r", "rb", "w", "wb", "a", "ab"]
        self._encoding = encoding or locale.getpreferredencoding()
        self._newline = newline or os.linesep
        if "w" not in self._mode:
            # make a request so we can see the self._size
            self._size = self._get_size()
            assert self._size is not None
        self._chunk = 1024
        self._initial_request = True
        assert upload_method in ["POST", "PUT"]
        self._upload_method = upload_method
        self._closed = False

    def tell(self):
        """Tell the position of the pointer."""
        return self._pos + 1

    def write(self, content):
        """Write content to file."""
        if "a" not in self._mode and "w" not in self._mode:
            raise Exception(f"write is not supported with mode {self._mode}")

        if "b" in self._mode:
            self._upload(content)
        else:
            self._upload(content.encode(self._encoding))

    def seekable(self):
        """Whether the file is seekable."""
        return "w" not in self._mode

    def read(self, length=-1):
        """Read the file from the current pointer position."""
        if self._pos >= self._size:
            return ""  # EOF
        if length < 0:
            end = self._size + length
        else:
            end = self._pos + length - 1
        if end >= self._size:
            end = self._size - 1
        result = self._request_range(self._pos, end)
        self._pos += len(result)
        if self._mode == "r":
            return result.decode(self._encoding)
        return result

    def readline(self, size=-1):
        """Read a line."""
        if self._mode == "r":
            terminator = self._newline
            result = ""
        else:
            terminator = b"\n"
            result = b""
        while True:
            ret = self.read(self._chunk)
            if ret == "":
                break
            if terminator in ret:
                used = ret.split(terminator)[0] + terminator
                unused = ret[len(used) :]
                # rollback
                self._pos -= len(unused)
                result += used
                break
            result += ret

            if size is not None and size > 0:
                if len(result) > size:
                    return result[:size]

        if not result:
            return ""
        return result

    def readlines(self, hint=-1):
        """Read all the lines."""
        if hint is None or hint < 0:
            hint = None

        lines = []
        while True:
            line = self.readline()
            if line == "":
                break
            else:
                lines.append(line)
            if hint and len(lines) >= hint:
                break
        return lines

    def seek(self, offset, whence=0):
        """Set the pointer position."""
        if whence == 0:
            self._pos = offset
        elif whence == 1:
            self._pos = self._pos + offset
        elif whence == 2:
            self._pos = self._size + offset
        if self._size is not None:
            if self._pos >= self._size:
                self._pos = self._size - 1
        return self._pos

    def _upload(self, content):
        if IS_PYODIDE:
            if self._initial_request and "a" not in self._mode:
                append = False
            else:
                append = True

            if self._upload_method == "POST":
                req = _sync_xhr_post(
                    self._url, content, "application/octet-stream", append
                )
            elif self._upload_method == "PUT":
                req = _sync_xhr_post(
                    self._url, content, "application/octet-stream", append
                )
            if req.status != 200:
                raise Exception(f"Failed to write: {req.response}, {req.status}")

            if self._initial_request:
                self._initial_request = False
        else:
            raise NotImplementedError

    def _get_size(self):
        if IS_PYODIDE:
            req = _sync_xhr_head(self._url)
            if req.status in [200]:
                length = req.getResponseHeader("Content-Length")
                return int(length)
            else:
                raise Exception(f"Failed to fetch: {req.status}")
        else:
            req = Request(self._url, method="HEAD")
            response = urlopen(req)
            if response.getcode() in [200]:
                length = response.info().getheader("Content-Length")
                return int(length)
            else:
                raise Exception(f"Failed to fetch: {response.getcode()}")

    def _request_range(self, start, end):
        assert isinstance(start, int) and isinstance(end, int)
        assert start <= end
        if IS_PYODIDE:
            req = _sync_xhr_get(self._url, start, end)
            if req.status in [200, 206]:
                result = req.response.to_py().tobytes()
                crange = req.getResponseHeader("Content-Range")
                if crange:
                    self._size = int(crange.split("/")[1])
            else:
                raise Exception(f"Failed to fetch: {req.status}")
        else:
            req = Request(self._url, method="GET")
            req.add_header("range", f"bytes={start}-{end}")
            response = urlopen(req)
            if response.getcode() in [200, 206]:
                crange = response.info().getheader("Content-Range")
                if crange:
                    self._size = int(crange.split("/")[1])
                result = response.read()
            else:
                raise Exception(f"Failed to fetch: {response.getcode()}")
        return result

    def close(self):
        """Close the file."""
        self._closed = True


def open_elfinder(path, mode="r", encoding=None, newline=None):
    """Open an HTTPFile from elFinder."""
    if not path.startswith("http"):
        url = location.origin + "/fs" + path
    else:
        url = path
    return HTTPFile(url, mode=mode, encoding=encoding, newline=newline, name=path)
