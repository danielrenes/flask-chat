# flask-chat

### Install required packages (Ubuntu):
```sh
sudo apt install python-dev python-virtualenv python-pip
```

### Go into the root of the project folder and create a virtual environment:
```sh
virtualenv venv
```

### Add the following line to the end of the venv/bin/activate script:
```sh
export FLASK_APP=flask-chat.py
```

### Activate the virtual environment:
```sh
source venv/bin/activate
```

### Install the requirements:
```sh
pip install --trusted-host pypi.python.org -r requirements.txt
```

### Start the app with the following command:
```sh
flask debug
```
