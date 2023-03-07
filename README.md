<!-- ABOUT THE PROJECT -->
## About kubectlpl command

Going through the pod logs of your local machine using `kubectl logs` can be a difficult task as it initially looks like a 
nonsense bunch of spaghetti json lines. I believe that finding info or debugging errors can be easier with just having 
some good format of the logs, so I created this command with that intention.

### Built With

* [![Python][Python]][Python-url]

### Installation

1. Clone the repo
   ```sh
   git clone https://github.anaplan.com/aldo-gonzalez/kubectlpl.git
   ```
2. Go to project folder and install the command
   ```sh
   sh installer.sh
   ```
3. If not already add your $HOME/bin folder to PATH env variable
   ```sh
   export PATH=\$PATH:\$HOME/bin"

<!-- USAGE EXAMPLES -->
## Usage

kubectlpl is basically a wrapper for "kubectl" command and "logs" option to pretty format the text output and filter by 
log level:
   ```sh
   kubectlpl (POD) [-c <container>] [-n <namespace>] [-s <since>] [-l <log-level>]
   ```

Normally using `kubectl logs` we could get some response as follows:

Kubectl command example:
```shell
kubectl logs -n some_name_space my_pod
```

Log sample in response:
```text
{"name":"some.class.name", "time": "2023-03-04 17:43:31,972", "location": "file.py:12", "level": "INFO", "message": "{"appName": 
"my-application-name", "class": "class.name", "sessionId": "", "logLevel": "INFO", "message": "A message in my log",  
"timestamp": "2023-03-04 17:43:31.972008", "traceId": "", "tracePath": "", "userId": ""}"}
```

So instead we could use kubectlpl and get a more readable response:

Kubectlpl command example:
```shell
kubectlpl -n some_namespace my_pod
```

Log sample in response:
```json
{
   "name": "some.class.name",
   "time": "2023-03-04 17:43:31,972",
   "location": "file.py:12",
   "level": "INFO",
   "message": {
      "appName": "my-application-name",
      "class": "class.name",
      "sessionId": "",
      "logLevel": "INFO",
      "message": "A message in my log",
      "timestamp": "2023-03-04 17:43:31.972008",
      "traceId": "",
      "tracePath": "",
      "userId": ""
   }
}
```

It also supports format for stack traces if present in the log:

Kubectl command example:
```sh
kubectl logs -n some_namespace my_pod my_container -s 1h
```

Log sample in response:
```text
{"appName": "MY_APP_NAME", "class": "class.name", "sessionId": "",  "exception": "'NoneType' object has no attribute 'get'",   
"logLevel": "ERROR", "message": "Exception received",   "stackTrace": "Traceback (most recent call last):\n  
File \"/path/to/file.py\", line 1, in method_name\n    \"some_key\": some_method(arg1, arg2),\nAttributeError: 'NoneType' 
object has no attribute 'get'\n", "timestamp": "2023-03-05 16:20:03.256699",  "tracePath": "", "userId": ""}
```

kubectlpl command example:

```shell
kubectlpl -n some_namespace my_pod my_container -s 1h -l ERROR
```

Log sample in response:
```json
{
  "appName": "MY_APP_NAME",
  "class": "class.name",
  "sessionId": "", 
  "exception": "'NoneType' object has no attribute 'get'",  
  "logLevel": "ERROR",
  "message": "Exception received", 
  "stackTrace": "Traceback (most recent call last):
	"/path/to/file.py" (1): method_name
		"some_key": some_method(arg1, arg2),
	Error  AttributeError: 'NoneType' object has no attribute 'get'",
  "timestamp": "2023-03-05 16:20:03.256699",
  "tracePath": "",
  "userId": ""
}
```

About filtering by logging we have set 4 levels of filter, so the response will contain every log below or same value as 
the level set in the command:

```python
ERROR = 1
DEBUG = 2
WARNING = 3
INFO = 4
```

For example requesting WARNING log level logs `kubectlpl -n some_namespace my_pod my_container -s 1h -l WARNING` will 
return all the logs with log level of warning, debug and error, also INFO will show every log even if is not a json 
string e.g. data related to initialization of the pod/containers.

Any error parsing a json string log will print as it was originally found with a message above for further investigation
and fix of such cases.

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python]: https://img.shields.io/badge/Python-145DA0?style=for-the-badge&logo=python&logoColor=yellow
[Python-url]: https://www.python.org/