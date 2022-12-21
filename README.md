# Скрипт для подачи заявлений в разделе ФССП Госуслуг

С помощью скрипта можно автоматически размещать заявления на сайте [Госуслуги].

Скрипт работает посредством автоматизации браузера Google Chrome. Закрытие браузера во время работы скрипта 
может привести к ошибке и не сохранению данных с результатами создания последнего обращения.

Необходимые данные для подачи заявления берутся из файла Microsoft Excel название которого задается 
в соответствующей настройке в файле config.txt.

Параметры указываемые в файле Microsoft Excel, необходимые для подачи заявления это:
1. Номер ИП
2. Ходатайство

При запуске скрипта организуется подача только тех заявлений для которых в файле Microsoft Excel
не указаны значения в столбцах:
1. Дата отправки
2. Номер заявления

Дополнительно к подаваемым заявлениям прикладывается PDF файл название которого также задается 
в соответствующей настройке в файле config.txt.

После автоматической подачи заявления пустые столбцы в файле Microsoft Excel заполняются 
автоматически, что позволяет избежать повторной отправки соответствующих заявлений.

Таким образом для подачи новых заявлений необходимо добавить новые строки в файле Microsoft Excel
заполнив столбцы **Номер ИП** и **Ходатайство**.

**ВАЖНО!!!** 
1. Названия столбцов в файле Microsoft Excel и параметров в файле config.txt менять нельзя!
2. Файл Microsoft Excel, PDF и config.txt нельзя редактировать во время работы скрпта.

Параметры необходимые для авторизации скрипта на сайте [Госуслуги] приведены в файле config.txt.

## Структура файла config.txt
```text
{
    "LOGIN": "+7**********",
    "PASSWORD": "*******",
    "TIMEOUT": "7",
    "ORGANIZATION": "1",
    "NAME_FILE_ORDER": "Вложение Приказ № 1 о назначении дир-ра ПАТРИОТ0001.pdf",
    "NAME_EXEL": "Ходатайства.xlsx"
}
```
где:

**LOGIN** - Номер телефона пользователя.

**PASSWORD** - Пароль пользователя.

**TIMEOUT** - Время задержки в секундах до выполнения следующего шага скриптом.

**ORGANIZATION** - Порядковый номер юридического лица на страницы *"Войти как"*. В случае если 
задать 0 вход будет осуществлен от частного лица.

**NAME_FILE_ORDER** - Название файла PDF который будет приложен к заявлению.

**NAME_EXEL** - Название файла Microsoft Excel из которого берутся данные для подачи заявления.

## Внешний вид таблицы Microsoft Excel

<table id="verticalalign">
<thead>
  <tr>
    <th>Номер ИП</th>
    <th>Ходатайство</th>
    <th>Дата отправки</th>
    <th>Номер заявления</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>77085/19/26023-ИП</td>
    <td>Прошу предоставить ифнормацию о ходе ИП</td>
    <td>09.11.2022</td>
    <td>2267915276</td>
  </tr>
  <tr>
    <td>77085/19/26023-ИП</td>
    <td>Новое обращение*</td>
    <td></td>
    <td></td>
  </tr>
</tbody>
</table>

**Новое обращение будет подано при запуске скрипта*


[Госуслуги]: https://esia.gosuslugi.ru/
