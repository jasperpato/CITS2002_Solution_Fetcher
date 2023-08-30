# CITS2002 Sample Solution Fetcher

### Project 1 2023

Fetches the sample solution measurements for a given sysconfig and commands file.

### Setup

Download the repo:

```console
$ git clone https://github.com/jasperpato/CITS2002-solution-fetcher.git
```

Create a python virtual environment:

```console
$ cd CITS2002-solution-fetcher
$ python3 -m venv venv
```

Activate the virtual environment:

```console
$ source venv/bin/activate
```

Install the required packages:

```console
$ pip3 install -r requirements.txt
```

Create a file named .env to store your private information:

```console
touch .env
```

Enter the sample solution webpage URL and your UWA credentials in .env:

```
url=https://...
username=username
password=password
```

### Usage

```console
$ python3 [--verbose] fetch_solution.py path/to/sysconfig_file path/to/commands_file
```
