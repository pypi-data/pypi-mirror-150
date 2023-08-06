# python-logger
A simple yet fancy logger for Python scripts

Each log has the following syntax:
```{filename}.py:{line} - [INFO-WARNING-DEBUG-ERROR]: log message```

## Install
- Using pip:
```shell
pip install lgg
```

- Using Poetry:
```shell
poetry add lgg
```

## Usage
```python
from lgg import get_logger
logger = get_logger()

logger.info('This is an info message')

logger.debug('Debugging message')

logger.error('error message')

logger.warning('File not found! An empty one is created')
```
![Result](.resources/overview.png)
