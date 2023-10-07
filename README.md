# codeforces-table-generator

## Добавление в свой репозиторий:
0. Созддайте файл ```codeforces_tasks``` в корне реозитория, там должен храниться список задач. На первой строке количество задач "по желанию", далее обязательные задачи.
Пример:
```
8
4A
617A
271A
263A
1352A
276A
1872A
978A
978B
1330A
1721B
1717B
1670B
1512C
1404A
```
1. Создайте workflow в своем репозитории:
```.github/workflows/cf_table.yml```
```yml
name: main_workflow_for_cf

on:
  push

permissions:
  contents: write

jobs:
  draw-table:
    uses: rdinit/codeforces-table-generator/.github/workflows/generate_md.yaml@v1
```

При каждом коммите файл с результатами будет обновляться.

## ToDo:
Автоматическое обновление списка задач по академической группе.
Деление на учебные блоки, например чтобы смотреть статистику за каждый семестр или другой временной период.