from fastapi import FastAPI
from starlette.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def root():
    return HTMLResponse(
        content="""
        <!doctype html>
        <html lang="ru">
        <head>
          <meta charset="utf-8" />
          <title></title>
          <link rel="stylesheet" href="style.css" />
        </head>
        <body>
         window.YaAuthSuggest.init(
    {
      client_id: "c865ee8244ea45b6b97d96421399ae1f",
      response_type: "token",
      redirect_uri: "https://cosm-report.podruge-apps.ru/"
    },
    "https://cosm-report.podruge-apps.ru",
    { view: "default" }
  )
  .then(({handler}) => handler())
  .then(data => console.log('Сообщение с токеном', data))
  .catch(error => console.log('Обработка ошибки', error))
        </body>
        </html>
        """
    )
