# Gate.io disperser

## Запуск под Windows
- Установите [Python 3.11](https://www.python.org/downloads/windows/). Не забудьте поставить галочку напротив "Add Python to PATH".
- Установите пакетный менеджер [Poetry](https://python-poetry.org/docs/). Не забудьте добавить Poetry в переменную окружения Path.
- Установите [git](https://git-scm.com/download/win).
- С помощью командной строки склонируйте этот репозиторий, после чего перейдите в него:
```bash
git clone https://github.com/AlenKimov/gate_disperser
cd gate_disperser
```
- Установите требуемые библиотеки с помощью Poetry и запустите скрипт:
```bash
poetry update
poetry run python start.py
```