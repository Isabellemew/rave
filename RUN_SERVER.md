Короткие инструкции для локального приёма заявок брони в CSV (открывается в Excel).

Шаги:

1) Создайте виртуальное окружение и установите зависимости:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
pip install -r requirements.txt
```

2) Запустите сервер (он будет слушать порт 5000):

```powershell
python server.py
```

3) Запустите статику (фронтенд) в другой консоли, например:

```powershell
python -m http.server 8000
```

4) Откройте в браузере:

http://localhost:8000/booking.html

5) После отправки формы данные будут добавляться в файл `bookings.csv` в корне проекта. Его можно открыть в Excel.

Примечания:
- Если сайт открыт по `file://` (двойной клик по index.html), браузер заблокирует fetch-запросы. Поэтому фронтенд надо запускать через http сервер (шаг 3).
- Если нужен экспорт в полноценный `.xlsx`, можно добавить библиотеку `openpyxl` и немного модифицировать `server.py`.

Google Sheets (опционально)

1) Создайте Google Spreadsheet и скопируйте его ID (часть URL после `/d/`).
2) Создайте сервис‑аккаунт в Google Cloud Console, создайте ключ в формате JSON и сохраните файл как `gs_credentials.json` в корне проекта.
3) Откройте созданную таблицу, нажмите Share и добавьте туда email сервис‑аккаунта (в формате `...@...gserviceaccount.com`) с правом редактирования.
4) Установите переменную окружения `GOOGLE_SHEET_ID` равной ID таблицы или полному URL таблицы. В PowerShell:

```powershell
$env:GOOGLE_SHEET_ID = 'ВАШ_SHEET_ID'
```

или

```powershell
$env:GOOGLE_SHEET_ID = 'https://docs.google.com/spreadsheets/d/ВАШ_SHEET_ID/edit'
```

5) Убедитесь, что зависимости установлены (`pip install -r requirements.txt`) — добавлены `gspread` и `google-auth`.

После этого сервер попытается автоматически отправлять новые брони и в Google Sheet (параллельно с `bookings.csv`). Если вы не хотите использовать Google Sheets — просто не создавайте `gs_credentials.json` и не устанавливайте `GOOGLE_SHEET_ID`.

