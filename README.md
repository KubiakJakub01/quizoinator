# quizoinator

## Setup

### With python virtualenv

Create a virtual environment and install the requirements:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then run the application:

```bash
python3 app.py
```

### With docker

Build the image:

```bash
docker build -t quizoinator .
```

Run the container:

```bash
docker run -p 5000:5000 -v ./instance:/app/instance -v ./src/static/user/images:/app/src/static/user/images quizoinator
```

### With docker-compose

```bash
docker-compose up
```
