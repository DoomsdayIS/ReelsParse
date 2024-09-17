# Reels // Shorts view parser

## Project Description

This project provides the ability to track InstagramReels and YoutubeShorts views for analytical and business purposes using various APIs.

## Installation

To get a working local version of this repository, you need to complete the following few steps.

> 1. Clone this repository
``` sh
$ git clone https://github.com/DoomsdayIS/ReelsParse
```

> 2. Install the required Python packages
```sh
$ pip install -r requirements.txt
```
## Usage

To run this project, you can use the already implemented derived classes from the MediaAPI and the Database.  In this case, you should simply provide your credentials in the instance constructors in the main.py

But you can also implement your own subclasses of the MediaAPI or Database abstract classes and use them

```python
class MediaAPI(metaclass=ABCMeta):
    @abstractmethod
    def create_request_arguments(self, url: str) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def get_views_from_response(response: httpx.Response) -> int:
        pass
```
```python
class Database(metaclass=ABCMeta):

    @abstractmethod
    def get_reels_urls(self) -> typing.List[str]:
        pass

    @abstractmethod
    def update_reels_views(self, reels_views: typing.Dict[str, int]):
        pass
```
