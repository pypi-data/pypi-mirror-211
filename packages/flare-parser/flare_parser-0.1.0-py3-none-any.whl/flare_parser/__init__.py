from typing import Any, Dict, Sequence
from dataclasses import dataclass
import yaml
import requests


@dataclass
class FlareChunk:
    uri: str


@dataclass
class FlareStream:
    name: str
    headers: Any
    content: Sequence[FlareChunk]


@dataclass
class FlareFile:
    uri: str
    streams: Dict[str, FlareStream]


def flare(uri):

    try:
        if uri.startswith('http'):
            data = requests.get(uri)
        else:
            with open(uri) as file:
                data = file.read()
    except:
        raise ValueError(f'Could not open file at `{uri}`')

    # Parse the file

    try:
        data = yaml.safe_load(data)

        file = FlareFile(uri, {})

        for stream_name, stream_data in data.items():
            stream = FlareStream(
                stream_name,
                stream_data.get('headers'),
                [],
            )

            for chunk_data in stream_data.get('content'):

                assert isinstance(chunk_data, str)
                stream.content.append(FlareChunk(chunk_data))

            file.streams[stream_name] = stream
    except:
        raise ValueError(f'Flare file is malformed')

    return file
