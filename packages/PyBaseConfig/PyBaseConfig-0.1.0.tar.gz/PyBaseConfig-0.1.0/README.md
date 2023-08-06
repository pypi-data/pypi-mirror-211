# PyBaseConfig

PyBaseConfig ist ein Python-Paket, das Ihnen beim Lesen und Verwalten Ihrer Umgebungsvariablen hilft. 

## Installation

Sie können dieses Paket mit pip installieren:


pip install pybaseconfig


## Verwendung

Hier ist ein Beispiel, wie Sie dieses Paket verwenden können:

```python
from pybaseconfig import BaseSettings

class Config(BaseSettings):
    email: str
    password: str
    server: str
    port: int

config = Config()
print(config.email)
```
