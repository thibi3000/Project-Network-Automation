# Project Network Automation 1

Python script to manage servers and automate tasks.
Works on Windows, Linux & macOS.

![Script](https://user-images.githubusercontent.com/23398694/116447187-3c22f380-a847-11eb-98fa-29089c0b5e81.png)

## Prerequisites

### Python 3.9.x

[Download here](https://www.python.org/downloads/)

### Clone the repository

```bash
git clone https://github.com/thibi3000/Project-Network-Automation.git
```

### Create a new virtual environment in the project folder

Highly recommended!

```bash
python -m venv venv
```

### Activate venv

#### Windows

```bash
activate.bat
```

#### Linux & macOS

```bash
source venv/bin/activate
```

### Update to the latest PIP version

```bash
python -m pip install --upgrade pip
```

### Install requirements

```bash
python -m pip install -r requirements.txt
```

### Install Vagrant

Vagrant 1.4 or greater (currently tested with 1.7.2). Using the latest version of Vagrant is strongly recommended.

[Download here](https://www.vagrantup.com/downloads)

### Install vbguest

```bash
vagrant plugin install vagrant-vbguest
```

### Install a Vagrant provider

#### VirtualBox

Must be installed on its own.
[Download here](https://www.virtualbox.org/wiki/Downloads)

## Usage

```bash
python main.py
```

## Documentation

### pydoc

```bash
python -m pydoc <scriptname>
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
