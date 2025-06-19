# Разворачивание Django-проекта на RedOS

## ✅ Требования

* RedOS / RHEL-подобная система
* Установленный `python3`, `pip`, `git`, `nginx`
* Статический IP

---

## ⚡ Подготовка

### Отключить SELinux (Обязательно)

```bash
sudo setenforce 0
sudo sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
```

### Установить зависимости:

```bash
sudo dnf install python3 python3-devel git gcc nginx redhat-rpm-config \
openldap-devel libxml2-devel libxslt-devel unixODBC-devel
```

---

## 📂 Клонирование и виртуальное окружение

```bash
cd /opt
GIT_SSL_NO_VERIFY=true git clone https://gitlab.solar.local/ВАШ_ПРОЕКТ.git myproject
cd myproject
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔧 Django: настройка

* Убедись, что в `settings.py`:

  * DEBUG = False
  * ALLOWED\_HOSTS = \['IP', 'домен']
  * STATIC\_ROOT установлен

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

---

## 🚀 Gunicorn

### Создаем gunicorn.service

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/opt/myproject
ExecStart=/opt/myproject/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/opt/myproject/gunicorn.sock \
          DjangoWebProject1.wsgi:application

[Install]
WantedBy=multi-user.target
```

> Замените `DjangoWebProject1` на свой python-модуль

```bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

---

## 🔌 NGINX

```nginx
server {
    listen 80;
    server_name ВАШ_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /opt/myproject;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/opt/myproject/gunicorn.sock;
    }
}
```

```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔄 Обновление проекта

```bash
cd /opt/myproject
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

---

## ✅ Готово!

Проект должен быть доступен по IP/домену.
