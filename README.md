
# Pager Station

![pager_main](docs/img/pager_main.png)

## Содержание
- [Что это такое](#что-это-такое)  
- [Список возможностей](#список-возможностей)  
- [Необходимое железо](#необходимое-железо)  
- [Подключение и установка на Raspberry Pi](#подключение-и-установка-на-raspberry-pi)  
- [Перепрограммирование пейджера](#перепрограммирование-пейджера)  
- [Первоначальная настройка](#первоначальная-настройка)  
- [Примеры использования](#примеры-использования)  
- [Использованные источники](#использованные-источники)  

## Про предыдущую версию
Предыдущая версия, основанная на Django+DRF+Celery, теперь заархивирована и находится в [соответствующей ветке](https://github.com/Galakart/PagerStation/tree/django-drf-celery "соответствующей ветке").

Данная версия, более облегчённая, основана на Fastapi.

## Что это такое
Простым языком: это программа (веб-приложение), с помощью которой вы сможете оживить свой старый пейджер, который уже давно валяется без дела, и отправлять на него сообщения.

Для программистов: это обёртка (REST-бэкенд) над замечательной программой **RPITX**, у которой, помимо всего прочего, есть возможность отправки в эфир сообщений по пейджинговому протоколу POCSAG. В качестве передатчика используется Raspberry Pi, на неё же и устанавливается весь сервис.

## Список возможностей
- отправка на пейджер личных сообщений;
- периодический сбор из интернета и отправка новостных сообщений (погода, курс валют, или заголовки любых RSS-лент);
- REST-API для отправки сообщений через GET и POST запросы, или управления из своих сервисов (из сторонних программ, мобильных приложений, умных колонок, итд);
- <details>
  <summary>TODO</summary>
  - минимальный веб-интерфейс для отправки сообщений;
  <br />  
  - веб-панель администратора для настроек;
</details>

Поддерживаются пейджеры модели **Motorola Advisor** (как на картинке в начале), так как по сути только он в наше время поддаётся перепрошивке (ну и ещё у него самый брутальный и узнаваемый вид, конечно же).  
Работа с другими пейджерами возможна, только при условии что известны их частота и капкод, по этому принципу был успешно опробован двухстрочный пейджер Navigator.

Дальность действия Raspberry Pi как передатчика (на скорости POCSAG 512) составляет примерно от 100 до 900 метров (сильно зависит от перекрытия стенами и домами).

## Необходимое железо
- собственно, сам пейджер Motorola Advisor, купленый на Авито во вменяемом состоянии;
- Raspberry Pi (а также карта памяти и блок питания). Подойдёт практически любая модель (смотрим на [системные требования](https://github.com/F5OEO/rpitx#hardware "системные требования") программы rpitx), было успешно опробовано на самой первой версии "Pi B" 2013 года;
- переходник USB to TTL - можно купить например на Озоне. Выглядит как небольшая платка с USB на одной стороне, и несколькими штырьками с другой;
- несколько проводков с разъёмами "мама" под одиночные штырьки;
- скорее всего, немного будет нужен паяльник и соответствующие навыки;

## Подключение и установка на Raspberry Pi
Берём в одну руку Raspberry Pi, а в другую - один проводок с разъёмами. Подключаем его к штырьку GPIO 4 (который седьмой по счёту) и оставляем болтаться - этот проводок у нас будет играть роль плохонькой антенны.

![rpi_gpio](docs/img/rpi_gpio.png)

Автор не особо силён в антенностроении, но эксперименты показали, что нет особой разницы, подключать кусок провода, или нормальную вертикальную жёсткую антенну - дальность действия будет примерно одинаковой. Длина антенны тут тоже особой роли не играет (конечно, слишком короткую не нужно делать, но разницы между 20см и 40см практически нет)

С подключением закончили, переходим к программной части.

Если мы ставим всё с нуля, то раскатываем на карту памяти образ свежей Raspberry Pi OS (она же в прошлом Raspbian). Подключаемся по SSH в консоль и первым делом запустим настройки.
```bash
sudo raspi-config
```

Главное что тут нужно поменять:
- сдвинуть доступную GPU Memory на минимум, освободив оперативку;
- расширить файловую систему на всю карту памяти (Expand Filesystem);
- по желанию можно разогнать процессор;

В конце потребуется перезагрузить систему.

Настраиваем часовой пояс, выбираем свой регион:
```bash
sudo dpkg-reconfigure tzdata
```

Обновляем систему:
```bash
sudo apt update
sudo apt dist-upgrade
sudo apt autoremove
```

По желанию, ставим русский язык:
```bash
sudo apt install language-pack-ru
sudo update-locale LANG=ru_RU.UTF-8
```

Устанавливаем всё необходимое ПО:
```bash
sudo apt install git python3-venv mariadb-server mariadb-client nginx
```

В домашней папке создаём ещё одну, в которой будем размещать этот проект. Назовём папку например, services, и зайдём в неё:
```bash
cd ~
mkdir services
cd services
```

Клонируем себе этот репозиторий и заходим внутрь папки:
```bash
git clone https://github.com/Galakart/PagerStation.git pagerstation
cd pagerstation
```

Далее условимся что папка с этим проектом находится по пути `/home/pi/services/pagerstation`  
Если она будет расположена в другом месте, меняем этот путь во всех нижеприведённых конфигах.

Установим rpitx:
```bash
git clone https://github.com/F5OEO/rpitx
cd rpitx
./install.sh
```

Ожидаем окончания сборки, соглашаемся на модификацию загрузочного файла, обязательно перезагружаемся
```bash
sudo reboot
```

Снова заходим в папку с проектом:
```bash
cd /home/pi/services/pagerstation
```

rpitx уже установлен, нам нужно взять только бинарник **pocsag**, положить его в корень проекта и навесить атрибут. Всё остальное можно удалить:
```bash
cp ./rpitx/pocsag ./pocsag
sudo rm -r ./rpitx
sudo chmod +x pocsag
```

По желанию, можно проверить работоспособность передатчика. Например попробуем что-нибудь отправить на частоте 89.7 FM. Если настроить любое радио (хоть в смартфоне) на эту волну, мы должны услышать характерный звук передачи:
```bash
echo "0000000:TEST" | sudo ./pocsag -f "89700000" -b 0 -t 1
```

Настроим MariaDB:
```bash
sudo mysql_secure_installation
```

- на вопрос о текущем пароле (current root password) просто нажать Enter (без пароля);
- на вопрос "установить пароль root?" (set root password) - говорим no, мы всё равно не будем использовать учётку рута;
- на все остальные вопросы отвечаем yes;

Далее создадим юзера БД, допустим с именем admin и паролем password, и новую БД для приложения:
```bash
sudo mariadb
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
CREATE DATABASE pagerstation CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit
```

В папке с программой создадим виртуальное окружение и активируем его:
```bash
python3 -m venv venv
source venv/bin/activate
```

Убедимся что мы в окружении - зелёное **venv** слева от командной строки (проверять в дальнейшем каждый раз, когда задействуем всё что связано с python из командной строки).

Скопируем и отредактируем файл настроек:
```bash
cp config.example.py config.py
nano config.py
```

- DB_NAME, DB_HOST, DB_USER, DB_PASS - параметры доступа к БД;
- OWM_TOKEN - токен OpenWeatherMap, который необходимо получить у них на сайте, для того чтобы работала отправка прогноза погоды;
- OWM_CITY - соответственно, город для OpenWeatherMap;

Установим зависимости, проведём миграции БД:
```bash
pip install -r requirements.txt
alembic upgrade head
```

Не знаю как будет в будущем, но на текущий момент в пакете PyOWM есть баг с получением прогноза погоды. Нужно вручную подправить файл в виртуальном окружении: venv/lib/python3.10/site-packages/pyowm/weatherapi25/national_weather_alert.py
```
assert sender поменять на assert sender is not None
assert description поменять на assert description is not None
```

**Переходим к настройке Nginx.**  
Создадим конфиг, удалив при этом стандартный:
```bash
sudo unlink /etc/nginx/sites-enabled/default
sudo nano /etc/nginx/sites-available/pagerstation
```

Вставим текст:
```bash
server {
    listen 80;

    location / {
      include proxy_params;
      proxy_pass http://unix:/home/pi/services/pagerstation/pagerstation.sock;
    }
}
```

Создадим ярлык, проверим конфигурацию, перезапустим Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/pagerstation /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

**Создадим конфиг для запуска самой программы:**
```bash
sudo nano /etc/systemd/system/pagerstation.service
```

Вставим текст:
```bash
[Unit]
Description=PagerStation service
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/home/pi/services/pagerstation
ExecStart=/home/pi/services/pagerstation/venv/bin/gunicorn main:app

[Install]
WantedBy=multi-user.target
```

Обновим и поставим в автозапуск:
```bash
sudo systemctl daemon-reload
sudo systemctl enable pagerstation
```

Теперь для ручного запуска можно вводить команду:
```bash
sudo service pagerstation start
```

Настройка завершена, для полной надёжности можно перезапустить систему, сервис стартует автоматически.

## Перепрограммирование пейджера
Желающие более плотнее ознакомиться с принципами работы пейджинговой связи, могут сделать это по ссылкам в конце этого текста. Тут я приведу только краткую выжимку.

Для начала ознакомимся с терминами:

- **абонентский номер**. Чаще всего - четырёхзначное число, присвоенное абоненту, чисто для удобства использования.

Его раньше называли оператору в телефоне, перед тем как надиктовать сообщение;

- **капкод (CAPCODE)**. Уникальный номер (максимум семизначный) вшитый оператором в пейджер во время программирования.

Именно на него передатчик шлёт сообщение, и именно он однозначно определяет, какое сообщение пейджер будет считать своим - принцип работы пейджинговой связи такой, что пейджер постоянно слушает эфир, и как только ловит принадлежащий ему капкод - то принимает и сохраняет следующее далее сообщение. Если это чужой капкод - то уходит в спячку до следующей передачи.  

Капкод и абонентский номер - это разные вещи, по той самой причине, что зная чужой капкод, можно запрограммировать свой пейджер на него и принимать чужие сообщения.  

Капкоды бывают трёх видов - личные, групповые, и новостные. Новостные и групповые капкоды во все пейджеры зашиваются одинаковые, чтобы одну посылку могли принять сразу все;  

- **источник**. Число от 0 до 3, передаётся в связке с капкодом, и задаёт, условно говоря, его подкатегорию.

Можно к примеру задать капкод 123456 и источник 0 - как абонентский номер 1111, а тот же капкод 123456 и источник 1 - как уже абонентский номер 1112, принадлежащий другому человеку.

Ещё можно например зашить в пейджер, что сообщения принятые на капкод 123456 и источник 2 - будут приниматься с принудительным громким оповещением, независимо от настроек беззвучности пейджера.

Касаемо новостных сообщений - используется для сортировки пейджером, так как новостные сообщения хранятся в памяти только последние, число источника указывает на ячейку памяти, в которой будет свежая информация о конкретной новости (погода, курсы валют, итд);

- **кодировка текста**. Бывает латинская, русская, и смешанная ("Linguist", у такой только заглавные буквы);

- **частота**. В мегагерцах, на которой пейджер принимает сообщения. По сути, сообщения передаются в аналоговом виде - звуком по радиоволне, это можно услышать любым радиоприёмником, если задать частоту в пределах FM-диапазона.

Для дальнейшей работы нам понадобится компьютер, на котором установлены:
- DOSBox (ибо софт для перепрошивки древний, написан под DOS);
- [Архив](https://drive.google.com/file/d/1NNrLwIHJ57ZtdJhKo3efF8boric_gJRj/view "Архив") с набором софта для прошивки;
- возможно драйвера на USB-TTL переходник;

Для начала выясним частоту пейджера. Тут не всё так просто - да, можно посмотреть что написано на задней крышке, но проблема в том что местные операторы в большинстве случаев скручивали частоты под свои передатчики. Так что, чтобы полностью удостовериться в правильности частоты, пейджер нужно разобрать, благо это делается вообще без винтов.

![pager_latch](docs/img/pager_latch.png)

Берём в руки пейджер, видим на нижней грани защёлку. Нам нужно с правой стороны её отогнуть ногтем от корпуса, а с левой толкать в правую сторону. Защёлка выйдет, после чего корпус распадётся на две половинки.  
Посередине мы видим плату, просто вставленную в гнездо. Это приёмник, нам нужно его отсоединить, и заглянуть вот сюда, под синюю обёртку.

![pager_receiver](docs/img/pager_receiver.png)

Нам нужно глянуть, что написано на этом кварце - некое число вроде 47.041. Это частота кварца, и чтобы нам получить из неё частоту пейджера, нужно её умножить на 3 и прибавить 17.9.  
То есть, 47.041 * 3 + 17.9 = 159.023 МГц - частота нашего пейджера. Эта формула работает только для Motorola Advisor, с другими - только надеятся на удачу.

Настало время самой сложной части - перепрошивка пейджера.

Снова берём пейджер в руки, и видим на его левом торце три отверстия, за которыми виднеются контакты. Это COM-порт, и через него мы будем подключать его к компьютеру. Контакты именуются, если слева направо и экраном вверх - Rx, Tx, GND. Соответственно, контакт для приёма данных, для передачи, и общий.

![pager_port](docs/img/pager_port.png)

Затем берём в руки наш USB-TTL-переходник, и видим на нём, как ни странно, те же самые контакты. Так вот, нам нужно нацепить три провода с разъёмами на одноимённые контакты переходника, а с другого конца разъёмы обрезаем, зачищаем проводки, и подключаем их в отверстия пейджера. 

Внимание - подключение идёт попарно! То есть, Rx переходника в Tx пейджера, и Tx переходника в Rx пейджера. Общий провод, понятное дело, одинаковый. Если на переходнике есть переключатель 3.3/5v, то желательно выставить 3.3, хотя в принципе нормально работает и на 5v.

Как закрепить провода в отверстиях - тут уж как фантазии хватит. Главное чтобы при самой прошивке контакт не нарушался, пейджеры этого не любят. Лично я делал так - приподнимал из корпуса основную плату с экраном, засовывал в отверстия корпуса проводки, затем опускал на место плату и она прижимала собой провода к контактам. Для надёжности можно прилепить их ещё изолентой к корпусу, чтобы случайно не вырвать. Главное чтоб контакты между собой внутри не замкнулись!

Вставляем в пейджер батарейку (можно его так и оставить полуразобранным, хоть с отсоединённым приёмником), и подключаем переходник к компу. Идём в Диспетчер устройств и запоминаем, на какой COM-порт у нас установился переходник (например, COM4). Если новых портов (кроме COM1-2) не появилось, то нужно установить драйвера на переходник.

Архив с ПО для прошивки разархивируем в отдельную папку, нечто вроде `D:\DOS\AdvisorTools`  
Проверяем чтобы внутри папки AdvisorTools лежал файл ADVCNFGF.ILE - он определяет что ПО установлено нормально.

Открываем конфиг DOSBox (в Пуске пункт меню DOSBox Options). Открывается текстовый файл настроек. В самый низ вставляем:
```bash
mount C D:\DOS\AdvisorTools
```

И чуть выше ищем пункт, что-то вроде serial1=dummy. Меняем его на:
```bash
serial1=directserial realport:com4
```

соответственно, вместо com4 указываем номер вашего переходника.
Запускаем DOSBox, переходим на диск C в папку moto, и запускаем ADVISOR.EXE
```bash
C:
cd moto
ADVISOR.EXE
```

![advisor_exe](docs/img/advisor_exe.png)

Первым делом жмём F9, переходим в настройки. Проверяем, чтобы пути соответствовали реальным (чтобы папка после C:\ действительно называлалсь "moto"), и чтобы был выставлен порт COM1. Если что, меняем, сохраняем, перезапускаем программу.

Жмём F3 - считываем данные из пейджера. Следим за переходником, во время передачи данных на нём быстро перемигиваются лампочки. Если это не так, или они не горят, то нужно проверить правильность всего вышеперечисленного, а также прочность контактов из проводков.

Здесь в большинстве случаев нас будет ждать облом - пейджеры почти всегда запаролены оператором от вмешательства. **ВНИМАНИЕ** - не стоит здесь пытаться подобрать пароль - пейджер выдержит несколько попыток, после чего заблокируется намертво (на нём будет гореть только надпись "ПЕЙДЖЕР ЗАБЛОКИРОВАН" или типа того) и его больше нельзя будет использовать даже как будильник!  
Однако ж, мы можем сбросить пароль (а также разблокировать пейджер, если всё же набедокурили здесь).

Для этого, отключаем пейджер от компа, разбираем его, и смотрим внимательно на основную плату:

![pager_hackwire](docs/img/pager_hackwire.png)

Это микросхема памяти, нас интересует одна отмеченая ножка - четвёртая слева.

Расчехляем паяльник и АККУРАТНО (не спаяв соседние ножки) припаиваем тонкий проводок к этому контакту. Второй его конец зажимаем на минусовую пружинку батарейки (батарейку тоже вставляем). Этим самым мы нарушили связь пейджера с его собственной прошивкой, и на экране скорее всего будет отображаться всякий мусор.

Снова подключаем пейджер к компу и запускаем DOSBox. Переходим на диск C, в папку moto\pass и запускаем RSS.EXE

Нажимаем пробел - по экрану побегут цифры и через несколько секунд замрут. Следим за процессом, если цифры долгое время циклически повторяются, и каждый раз пейджер начинает истерично пищать - нужно остановиться и проверить качество припаянного проводка, так как при плохом контакте пейджер воспринимает взлом как попытки перебора пароля и блокируется как описано выше.

Если цифры замерли и больше не реагируют на пробел, закрываем программу, отключаем батарейку и провод от минусового контакта, и пробуем всё заново - вставляем батарейку, подключаемся через программу ADVISOR.EXE и пробуем считать настройки кнопкой F3.  
Разблокировка может пройти не с первого раза, поэтому провод от микросхемы не отпаиваем и пробуем ещё раз. Если настройки успешно считались, то провод можно отпаять (или оторвать) и забыть об этом - пароль сброшен. Точнее, сбрасывается не пароль, а флаг о том что нужно его запрашивать.

После всего этого, мы можем видеть (и менять) настройки, загруженные из пейджера. Они расположены на нескольких страницах, переключение между ними идёт по нажатию PageUp/PageDown. Все пункты настроек описывать не буду, только самые основные. На каждом пункте можно нажать F1 и прочитать, что он означает.

![advisor_exe_capcodes](docs/img/advisor_exe_capcodes.png)

На первой странице мы видим в частности Serial # - серийный номер пейджера. Поменять нельзя, но можно сохранить куда-нибудь себе для аутентичности, в случае повреждения прошивки пейджер спросит новый серийный номер. Кстати, этот же номер считывается со штрих-кода на задней крышке пейджера.

Выставим **Coding Format** - оно же скорость передачи, по желанию, к примеру **POCSAG 1200**. 512 - медленнее, но стабильнее и больше радиус приёма. 1200 посередине. 2400 соответственно ровно наоборот.

Далее мы видим то, над чем придётся поднапрячь мозги - капкоды и их настройки. Более подробно вся эта тема раскрывается по ссылке в конце, в разделе использованных источников. В принципе, если неохота заморачиваться изменением капкодов, можно просто тут запомнить себе, какие капкоды зашил в пейджер последний оператор. Лишь бы были личные и новостные.

- У пейджера может быть 4 капкода (соответственно, Code A B C D), каждый из которых ещё подразделяется четырьмя источниками;
- Code Type - тип данного капкода
  + Individual - личный
  + Group - групповой
  + Mail Drop - новостной
- Цифры 1234 посередине - это обозначения источников (вообще они идут с нуля - 0123);
- Functions T,A,N,X - как будет воспринято сообщение, принятое на данный капкод+источник
  + A - как обычное текстовое;
  + N - "числовое" (это про старую кодировку, передающую только цифры);
  + T - тональное (сообщение без текста, пейджер просто запищит);
  + X - сообщение будет отброшено (используется, если мы раздаём один капкод нескольким абонентам, и делаем различие только в источниках);
- Priority Y,N - сообщение с источником, отмеченным тут как Y, будет принято со звуковым сигналом, независимо от настроек беззвучности пейджера;

А теперь, главное внимание, особо мозговыносящая вещь!
Капкоды должны вручную задаваться не абы как, а должны правильно располагаться попарно в одинаковых фреймах (пачках передаваемых данных)! То есть, Code A и Code B должны располагаться в одном фрейме, Code C и Code D - во втором. Причём второй должен быть больше первого. Программа конечно предупредит, если что-то не так, но всё же знать надо. Нарушение этого приведёт к сокращению вдвое времени работы от батарейки - пейджеру придётся чаще просыпаться для проверки посылок.

Как узнать номер фрейма? Есть встроенный калькулятор, достаточно перейти по ссылке http://IP_RASPBERRY/capcode_to_frame/234, где 234 это номер предполагаемого капкода.

В ответ он выдаст JSON с номером фрейма
```
{"frame_number":2}
```

Всего фреймов 8 (от 0 до 7). При увеличении капкода на 1, фрейм тоже увеличивается на 1, пока не дойдёт до 7, дальше отсчёт снова пойдёт с нуля. То есть к примеру, капкоды 525349 и 37 - относятся к 5-му фрейму, и их можно использовать в паре.  
По тому же принципу делаем вторую пару капкодов, к примеру 191 и 199 - фрейм у них будет 7-ой, и он больше чем 5-ый.
Ну и ещё - не рекомендуется использовать слишком мелкие капкоды (от 0 до 8).

Если всё вышеперечисленное непонятно (я тоже долго не мог понять), то просто делаем как я:

Капкод Code A задаём **0525349**, функции выставляем **ATXX**, приоритет **NNNN**, Code Type - **Individual**  
Капкод Code B задаём **0000037**, функции выставляем **AAXX**, приоритет **YNNN**, Code Type - **Group**  
Капкод Code C задаём **0000191**, функции выставляем **AAAA**, приоритет **NNNN**, Code Type - **Mail Drop**  
Капкод Code D задаём **0000199**, функции выставляем **AAAA**, приоритет **NNNN**, Code Type - **Mail Drop**  

Что мы имеем из всего этого?

- Сообщение на капкод **525349** + источник **0**  
принимается как личное в обычном текстовом виде, будет храниться на экране в 1-ой строке;
- Сообщение на капкод **525349** + источник **1**  
принимается как личное в тоновом виде (просто запищит с надписью ТОНОВЫЙ), будет храниться на экране в 1-ой строке;
- Сообщение на капкод **525349** + источник **2**  
будет отброшено;
- Сообщение на капкод **525349** + источник **3**  
будет отброшено;
- Сообщение на капкод **37** + источник **0**  
принимается как групповое с громким оповещением, независимо от режима беззвучности, будет храниться на экране в 1-ой строке, с пометкой ГРУППА;
- Сообщение на капкод **37** + источник **1**  
принимается как групповое, будет храниться на экране в 1-ой строке с пометкой ГРУППА;
- Сообщение на капкод **37** + источник **2**  
будет отброшено;
- Сообщение на капкод **37** + источник **3**  
будет отброшено;
- Сообщение на капкод **191** + источник **0**  
принимается как новостное и будет храниться на экране во 2-ой строке и 9-ой ячейке (например, чисто для погоды);
- Сообщение на капкод **191** + источник **1**  
принимается как новостное и будет храниться на экране во 2-ой строке и 10-ой ячейке (например, чисто для гороскопа);
- Сообщение на капкод **191** + источник **2**  
принимается как новостное и будет храниться на экране во 2-ой строке и 11-ой ячейке (например для... и так далее, каждая новостная категория в своей ячейке);
- Сообщение на капкод **191** + источник **3**  
принимается как новостное и будет храниться на экране во 2-ой строке и 12-ой ячейке;
- Сообщение на капкод **199** + источник **0**  
принимается как новостное и будет храниться на экране во 2-ой строке и 13-ой ячейке;
- Сообщение на капкод **199** + источник **1**  
принимается как новостное и будет храниться на экране во 2-ой строке и 14-ой ячейке;
- Сообщение на капкод **199** + источник **2**  
принимается как новостное и будет храниться на экране во 2-ой строке и 15-ой ячейке;
- Сообщение на капкод **199** + источник **3**  
принимается как новостное и будет храниться на экране во 2-ой строке и 16-ой ячейке;

Закончив наконец с капкодами, переходим на следующую страницу настроек (PageDown). На остальных страницах настраиваем всё по своему вкусу.

На третьей странице проверим чтобы **Data Inversion** стояла **No** (можно поиграться с этим параметром, если пейджер ни в какую не желает принимать сообщения).

На четвёртой странице можно задать собственные служебные строки (название оператора, или уведомления вроде "УДАЛИТЬ?" и "ЗАМЕНИТЕ БАТ.").

Наконец на самой последней странице, проверив что наш пейджер до сих пор включён и крепко подсоединён проводами, можно нажать F4 и запрограммировать изменения в пейджер. Если здесь будет нарушен контакт с проводами - прошивка слетит, появится мусор на экране, придётся всё настраивать с нуля.

В случае успешной прошивки пейджер перезагрузится, запищит, и на этом месте можно его отсоединять от компьютера, собирать обратно и переходить (запомнив конечно, что за номера мы в него внесли) к настройке собственно программы.

## Первоначальная настройка (TODO)
<details>
  <summary>TODO</summary>
  
Заходим на IP-адрес нашей Raspberry Pi, в раздел администрирования:  
http://192.168.1.123/admin/  
Вводим логин/пароль, который создавали ранее командой createsuperuser.

Отправлять сообщения напрямую (по частоте, капкоду, итд) можно без настроек, но для того чтобы отправлять по абонентскому номеру или получать новостную рассылку, их нужно произвести.

Для начала в левой панели переходим в **Transmitters**, создаём там новый, условно говоря "передатчик", введём:
- имя (например "Motorola");
- частоту (в герцах, например 158125000);
- скорость передачи, которую мы прошивали в пейджер (512, 1200, 2400);

Если у нас несколько пейджеров, работающих на разных частотах, для каждой частоты создаём свой "передатчик".

Затем переходим в раздел **Pagers**. Здесь мы собственно будем задавать параметры конкретного пейджера:
- его абонентский номер (в пейджер он не прошивается, так что здесь придумать свой);
- личный капкод;
- личный источник;
- кодировка текста;
- трансмиттер;

Затем идём в раздел **Clients**. Тут мы зададим образно говоря, абонента нашей супер пейджинговой станции:
- ФИО;
- дата рождения (чтобы в будущем рассылать поздравления);
- в выпадающем списке выделяем абонентские номера, которые будут ему принадлежать;

Идём в раздел **NewsChannels**. Здесь мы зададим параметры новостных рассылок:
- категория (погода, гороскоп, итд);
- новостной капкод;
- источник;
- кодировка текста;
- трансмиттер;

Суть раздела NewsChannels в том, чтобы программа отправляла одинаковое новостное сообщение (с одинаковой категорией) на разные трансмиттеры или новостные капкоды. Но если пейджер у нас ровно один, это не имеет значения.

Вот и всё, настройка завершена, на пейджер будет приходить новостная рассылка, а мы теперь сможем отправлять сообщения на абонентский номер.

</details>

## Примеры использования (TODO)
<details>
  <summary>TODO</summary>

В качестве примера будем отправлять личное сообщение на абонентский номер.

##### 1. С помощью веб-интерфейса DRF
Заходим в браузере на IP-адрес Raspberry Pi, в раздел API (там же доступно полное описание для сторонних сервисов): http://192.168.1.123/api  

Там мы видим доступные нам возможности, в виде ссылок. Выбираем отправку личных сообщений - http://192.168.1.123/api/privatemessages/

Открывается минимальный интерфейс, достаточный для отправки. Мы просто вводим в поля абонентский номер и текст сообщения, после чего кнопкой отправляем его.

Если мы не производили настройки абонента, то можно отправить сообщение напрямую по ссылке http://192.168.1.123/api/directmessages/ - нужно будет указать частоту, капкод, и прочее.

##### 2. С помощью POST запроса к REST-API
Для примера, выполним следующий код в консоли на любом компьютере, в локальной сети:
```bash
curl -X POST http://192.168.1.123/api/privatemessages/ -H 'Content-Type: application/json' -d '{"subscriber_number":"1234","message":"Привет всем!"}'
```
(соответственно, подставить свои IP-адрес, абонентский номер, текст сообщения)

</details>

## Использованные источники

#### Статьи и видео
- видео на канале **Hot Pixel:**  
https://www.youtube.com/watch?v=ukmvlHdsdfc
- две замечательные статьи от **SinuX:**  
https://mysku.ru/blog/diy/88396.html  
https://mysku.ru/blog/diy/88811.html  
- описание принципов формирования капкодов и их применения в Motorola Advisor, на **cxem.net**:  
https://cxem.net/telefon/2-28.php

#### Сторонние программы и сервисы
- разумеется, программа RPITX от автора F5OEO, при помощи которой и идёт вся отправка в эфир:  
https://github.com/F5OEO/rpitx
- сервис OpenWeatherMap, и оболочка PyOWM - для вытягивания прогноза погоды:  
https://openweathermap.org/  
https://pyowm.readthedocs.io/en/latest/
- сервис CoinGate - курсы валют:  
https://developer.coingate.com/docs

Поддержать автора  
BTC: bc1q5aptd289qsvrtsf9t2z42udda5t70e7hc39sc2
