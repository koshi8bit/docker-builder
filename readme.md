# docker-builder

Этот проект помогает работать из под винды в любимой среде разработки, но при этом 
собирать Docker контейнеры на Линухе **одним** батником

## Как это работает
В папке с проектом должно лежать два батника *push.bat* или *restart.bat* 
* push.bat нужен для билда и загрузки контейнера в dockerhub.
* restart.bat нужен для билда и (пере)запуска контейнера

При запуске батника запускается скрипт на python, который читает настройки из *.env* файла в каталоге *docker-builder* и делает следующее:
1. Очищает временный каталог (по дефолту **to_build**), который должен быть в папке с проектом
1. Перемещает файлы, указанные в **files.txt** во временный каталог
1. Очищает папку на удаленной linux машине через утилиту *putty*
1. Копирует файлы из временной папки на линукс машину через утилиту *pscp*
1. Билдит контейнер (пока метку нельзя ставить, но скоро добавлю)
1. Если был запущен батник *restart.bat* - то запускается процедура запуска контейнера (одного или нескольких). Процедура запуска описана в файле **restart.sh** (copy.py **-r**)
1. Если был запущен батник *push.bat* - то запускается процедура загрузки контейнера в dockerhub (copy.py **-r -p**)

## Что нужно 
* Скачать **putty и pscp** [тут](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
* Настроить запуск docker без sudo [(полная статья)](https://docs.docker.com/engine/install/linux-postinstall/):
  * `sudo groupadd docker`
  * `sudo usermod -aG docker $USER`
  * Перезагрузить виртуальную машину
* Скопировать нижеописанное в свой каталог с проектом
  * Папку docker-builder с содержимым
  * Файл push.bat и restart.bat
  * В папке с проектом создать папку **to_build** (попозже сделаю авто создание)
* Скопировать файл **.env_template** в **.env** папке docker-builder
* Заполнить файл **.env** 
* Заполнить файл **files.txt** путями файлов, из которых будет строиться контейнер   
* Заполнить файл **clear.sh** командами для очистки проекта (по дефолту удаляется все из папки). Для автоподстановки пути используется переменная **{dest_folder}** (пример в папке docker-builder)
* Заполнить файл **restart.sh** командами для остановки и запуска контейнера (пример в папке docker-builder)
* PROFIT! Осталось лишь запускать батники для автоматического развертывания

 
