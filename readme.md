# IRENS_MANSCRAPER
Эксплуатация и первый запуск:
 * Для активации на компьютере должен быть питон версии 3.6 и выше (совет - не устанавливайте 3.9, с ней пока много проблем, 3.7, 3.6 - рекомендую)
(гайдик в интернете гляньте как установить, займет минут 5)
 * Для начала нужно зайти в командную строку и прописать 
команду : cd путь/до/irens_teleth ( вместо путь и до скопируйте путь)
 * После нужно прописать при ПЕРВОМ запуске ( для установки модулей)
такую команду ( в ком. строку) : pip install -r requirements.txt
 * Теперь нужно проверить файл .env - открыть его можно любым текстовым редактором
там проверить все данные - а именно хост, юзер и т д, API_HASH и API_ID лучше не трогайте,
это телеграмовское апи, но если хотите - можете поставить свои.
 * Далее после установки всех нужных модулей прописываем следующую
команду : python irens_manscraper.py
 * Сначала появится запрос - через сколько секунд повторно делать запрос в базу 
и писать в телегу ребятам ( Подсказка - минута=60, час=3600, 24 часа = 86400)
числа с плавающей запятой писать не стоит, может ошибиться
* После, при ПЕРВОМ запуске, запросит номер телефона (Прим +380123456789) и код, высланный как сообщение в телеге, после того как впишете создастся файлик с сессией и
скрипт начнет действовать
* После в начале и каждые n секунд, указанных вами скрипт будет отправлять сообщения каждому админу( с     интервалом 2.5 секунд на 1 человека ( чтоб не было бана за спам))
  такое сообщение :
 "Привет, у тебя есть переводчики, не имеющие баланса уже                                               
 более 3-х дней и их надо уволить через сферу, либо отписать                                             
 мне, почему это делать не надо :                                                                       
   *-* Имя Фамилия,                                                                                         
   *-* Имя Фамилия."                                                                                         
 и писать в консоль скольким админам отправил сообщение (прим "-18:45:52 Отправлено 12 админам(у)") 
* Чтобы выйти из программы - нажмите Ctrl+C
* Чтобы поменять аккаунт просто удалите .session или переместите его из директории(чтобы в будущем использовать)
* По всем вопросам в тг - @work_to_die
