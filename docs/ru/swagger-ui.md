\# Swagger UI (интерактивная документация API)



\## Запуск Swagger UI локально



Сгенерированная OpenAPI спецификация доступна в файле \[openapi\_generated.json](https://github.com/gopstopsisi2-dotcom/my-docs/blob/main/api/openapi\_generated.json).



Для просмотра интерактивной документации:



\### Способ 1: Через Swagger Editor



1\. Перейдите на https://editor.swagger.io

2\. File → Import file → выберите `api/openapi\_generated.json`



\### Способ 2: Через Swagger UI (локально)



```bash

npx swagger-ui-watcher api/openapi\_generated.json



