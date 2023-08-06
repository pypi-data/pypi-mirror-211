# Script-Master

Сервис, который по конфигам (формат YAML), 
создает задания запуска скриптов в сервисе [Process-Executor](https://github.com/pavelmaksimov/process-executor),
согласно плану запусков полученных от сервиса [Work-Planner](https://github.com/pavelmaksimov/work-planner).

Отлично подходит для запуска ETL скриптов по расписанию.

Требует мало ресурсов, не требует БД, конфигурации скриптов 
и их параметры запуска (расписание) создаются в YAML конфигах, 
поэтому интерфейс не требуется, но он есть, дополнительно можно поставить.


## Install
    poetry add script-master

or

    pip install script-master

## Run
    script-master --help
    script-master init # Создаст конфиг в текущий директории
    script-master run # Запускать всегда в директории, в которой был выполнен init

or 
    
    uvicorn script_master.main:app --port 8080 --reload


## Интерфейс
Есть [интерфейс](https://github.com/pavelmaksimov/script-master-helper), он не обязателен. Для сервиса требуются только конфиги yaml, их иожно вручную создавать
Запускается отдельно/