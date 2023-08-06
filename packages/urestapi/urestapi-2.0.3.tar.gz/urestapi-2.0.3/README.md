# urestapi

A command-line client for Uptycs that has ability to run Uptycs restAPI

## Installation

If you already know how to install python packages, then you can install it via pip:

You might need sudo on linux.
if you want to install using pip, you can use following command:
```
$ sudo pip install urestapi
```

if you want to install from source you can use following command:
```
$ git pull urestapi
$ cd urestapi
$ python setup.py install
```

## Usage
```
    $ urestapi --help
    
Usage: urestapi [OPTIONS]

Options:
  -V, --version                   Output urestapi's version.
  -k, --keyfile TEXT              Uptycs json key file.
  --domainsuffix TEXT             Uptycs Domain Suffix like .uptycs.io
  --enable-ssl / --disable-ssl    verify ssl certificate
  -m, --method TEXT               restAPI method [GET|POST|PUT|DELETE]]
  -a, --api TEXT                  API name [/alerts, /assets, etc]
  -d, --postdata TEXT             post json data
  -D, --postdatafile TEXT         post json data file
  -f, --location TEXT             download location for package
  --threat_source_name TEXT       Name of the threatsource
  --threat_source_description TEXT
                                  description of the threatsource
  --threat_data_csv TEXT          csv file of the threatsource
  --help                          Show this message and exit.
```
