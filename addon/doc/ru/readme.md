# Часовые пояса
Дополнение для NVDA для объявления времени в выбранных часовых поясах.

## Информация
* Автор: Мунавар Биджани
* Скачать [стабильную версию][1]
* Совместимость: NVDA 2021.1 и более поздние версии
 
## Введение
Уже очень долгое время в Windows существует возможность отображения нескольких часов из разных часовых поясов. Пользователи могут настраивать часы, и они становятся мгновенно видимыми.

К сожалению, для пользователей программ чтения экрана, таких как [NVDA](https://www.nvaccess.org/) или [JAWS](http://www.freedomscientific.com), не существует простого способа получить эту информацию. Эти программы чтения экрана не поддерживают дополнительные часы, поэтому незрячим пользователям приходится прибегать к другим, сторонним решениям, некоторые из которых являются платными.

Многое в моей работе связано с работой в разных часовых поясах, и в конце концов я устал вручную переводить время в голове, особенно для часовых поясов, которые не выровнены по часам (например, Индия, где +5:30 по Гринвичу).

По этим причинам я создал это дополнение для NVDA. Дополнение позволяет вам услышать время в выбранных часовых поясах с помощью "кольца часовых поясов".

## Использование
Вы можете [скачать последнюю версию здесь][1]. Дополнение поддерживает как устаревшую версию NVDA, так и версию Python 3.

После установки дополнения вы можете настроить его, активировав диалог настроек NVDA и спустившись в категорию "Часовые пояса".

Выберите элементы в списке часовых поясов, чтобы добавить их в кольцо часовых поясов. Снимите выделение (или нажмите кнопку "Удалить"), чтобы удалить их из кольца.

Вы также можете изменить порядок временных зон в кольце с помощью кнопок "Переместить вверх" и "Переместить вниз".

Используйте поле "Фильтр" для поиска определенных часовых поясов.

Установите флажок "Объявлять сокращенные часовые пояса", чтобы услышать сокращенные названия часовых поясов, например IST или GMT. Снимите флажок, чтобы слышать полные названия часовых поясов, например Азия/Кольката или Европа/Лондон.

Вы можете настроить информацию, которую вы услышите при запросе времени в часовом поясе, установив/сняв флажки в группе "Компоненты":

* Континент: Объявить континент для текущего часового пояса.
* Страна: Объявить страну для текущего часового пояса.
* Город: Объявить город для текущего часового пояса.
* Время: Объявить время для текущего часового пояса.
* Дата: Объявить дату для текущего часового пояса.
* Объявить часовой пояс в (начале или конце): Произнесите часовой пояс первым или последним. Например, если вы хотите услышать "BST 9:42 AM", выберите радиокнопку "Начало". Если вы хотите услышать "9:42 AM (BST)", выберите радиокнопку "Конец".

Когда вы закончите настройку параметров, нажмите кнопку "OK".

С этого момента вы можете нажимать следующие кнопки для объявления времени в вашем часовом поясе:

* NVDA+ALT+Стрелка вверх: Объявление предыдущего часового пояса.
* NVDA+ALT+стрелка вниз: объявление следующего часового пояса.
* NVDA+ALT+T: Объявление последнего часового пояса, на который вы указывали в кольце часовых поясов. Нажатие этой клавиши несколько раз подряд приведет к перемещению вперед по кольцу часовых поясов, но не изменит часовой пояс, на который вы указываете.
* Для настройки этих клавиш используйте категорию "Часовые пояса" в диалоговом окне "Жесты ввода".

Когда вы впервые устанавливаете дополнение, NVDA по умолчанию будет использовать ваш локальный часовой пояс, если сможет его получить.
 ## Благодарности
Спасибо [@ruifontes](https://github.com/ruifontes) за существенную помощь в приведении этого дополнения в соответствие с рекомендациями по коду дополнений NVAccess. Спасибо Myla за тестирование дополнения на NVDA 2019.2.

### Перевод

* Русский, Валентин Куприянов
[NVDA.RU](https://nvda.ru/)

## Журнал изменений

### Версия 3.01, выпущена 26.03.2022

- Блокировка дополнения от запуска в безопасном режиме NVDA.

### Версия 3.00, выпущена 03/24/2022

- Теперь совместима с версией 2022.1 NVDA.
- Исправлена проблема, когда при перезагрузке дополнения отображались две категории конфигурации ([#10](https://github.com/munawarb/NVDA-Time-Zoner/issues/10)).

### Версия 2.00, выпущена 07/14/2021
- Теперь совместимо с версией 2021.1 NVDA.
- КРАТКОЕ ИЗМЕНЕНИЕ: Это дополнение больше не совместимо с устаревшими версиями NVDA. Пожалуйста, используйте версию 1.06 или более раннюю для поддержки устаревших версий.

### Версия 1.05, выпущена 07/26/2020.
- Исправлена ошибка при объявлении общих часовых поясов, таких как UTC или EST ([#7](https://github.com/munawarb/NVDA-Time-Zoner/issues/7)).

### Версия 1.04, выпущена 04/19/2020
- Объявление часовых поясов теперь настраивается. Кроме того, при нажатии NVDA+ALT+UP ARROW или NVDA+ALT+DOWN ARROW происходит циклический переход по кольцу часовых поясов, что делает дополнение удобным для конфигураций с большим количеством установленных часовых поясов ([#6](https://github.com/munawarb/NVDA-Time-Zoner/issues/6)).
- Диалог "Жесты ввода" использует новую категорию "Часовые пояса", чтобы облегчить поиск жестов для дополнения Часовые пояса ([#5](https://github.com/munawarb/NVDA-Time-Zoner/issues/5)).
- Настройки конфигурируются с помощью диалога "Настройки NVDA", а не через отдельный диалог.

### Версия 1.03, выпущена 03/21/2020.
- Дополнение больше не аварийно завершает работу, если не удается установить часовой пояс по умолчанию.
- Исправлена проблема с относительными ссылками в документации.

### Версия 1.02, выпущена 18.03.2020.
- При установке новой версии этого дополнения настройки предыдущей установки больше не теряются.
- Другие изменения для соответствия стандарту дополнения NVDA.

### Версия 1.01, выпущена 03/12/2020.
- Время и дата объявляются в локали пользователя, то есть, если установлено 24-часовое время.
- NVDA будет объявлять либо сокращенное, либо полное время в зависимости от настроек пользователя в диалоге "Кольцо часовых поясов". Например, он будет говорить либо Европа/Лондон, либо GMT или BST. Эта настройка контролируется установкой или снятием флажка "Объявлять сокращенные часовые пояса".
- Дополнение включает комментарии переводчиков (@ruifontes.)
- Дополнение теперь включает комментарии к заголовкам (@ruifontes.)
- Клавиша Escape закрывает диалог "Кольцо часовых поясов" (@ruifontes.)
- Пункт меню для открытия диалога "Кольцо часовых поясов" теперь называется соответствующим образом (@ruifontes.)
- NVDA теперь по умолчанию устанавливает местный часовой пояс при установке этого дополнения, если местный часовой пояс доступен.
- Поддержка нескольких часовых поясов с помощью кольца часовых поясов.
- Это дополнение теперь использует клавишу NVDA+ALT+T для предотвращения конфликта с дополнением Clock.
- Диалог выбора часового пояса теперь имеет поле фильтра. NVDA будет объявлять количество результатов, когда пользователь начнет вводить текст в поле фильтра.
- Поддержка Python 2
- Дата и время теперь объявляются в отдельном потоке, чтобы предотвратить зависание потока NVDA в случае, если поиск занимает некоторое время.
- Диалог выбора часового пояса теперь имеет кнопку отмены и больше не препятствует выключению NVDA.

[1]: https://github.com/munawarb/NVDA-Time-Zoner/releases/latest
 