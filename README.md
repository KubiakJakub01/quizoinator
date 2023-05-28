# quizoinator

## Setup

After successful setup, the application will be available at http://localhost:5000

### Prerequisites:

#### Clone the repository

```bash
git clone https://github.com/KubiakJakub01/quizoinator.git 
cd quizoinator
```

#### Install python3

Linux:
```bash
sudo apt install python3
```

Windows:
```bash
https://www.python.org/downloads/windows/
```

MacOS:
https://www.python.org/downloads/mac-osx/

For MacOS you can also use Homebrew:
```bash
brew install python3
```
For more information visit:
```bash
https://docs.python-guide.org/starting/install3/osx/
```

#### Install pip

Follow the instructions on: https://pip.pypa.io/en/stable/installation/ to install pip.

#### Docker (optional)

Follow the instructions on: https://docs.docker.com/get-docker/ to install docker.

### With python virtualenv

Create a virtual environment and install the requirements:

#### Linux and MacOS

```bash
python3 -m venv .venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Windows

```bash
python -m venv .venv
.\venv\Scripts\activate
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
docker compose up
```
