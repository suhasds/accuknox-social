# AccuKnox Project

This is an assignment project for AccuKnox.

### Project Setup

```
sudo apt-get update
sudo apt-get nginx
sudo apt-get install python3.10-dev git
sudo apt-get install build-essential libssl-dev libffi-dev
sudo apt-get install libjpeg-dev libfreetype6-dev zlib1g-dev

sudo apt-get install virtualenv
sudo apt-get install --upgrade pip

cd accuknox-social

virtualenv --python=python3.12 venv
source venv/bin/activate

pip install -r requirements.txt
```

### Create ENV

```
sudo nano .env
environment=local
save and exit
```

### Django Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Django Superuser

```bash
python manage.py createsuperuser 
```


### Run Django app

```bash
python manage.py runserver 
```
