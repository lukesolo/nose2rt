# nose2rt - nose2 data collector for Testgr

Plugin for sending HTTP POST updates to your **Testgr** service.

### Installing

```pip install nose2rt```

Find your nose2 config file and configure as described below.

Example:

```
[unittest]
plugins = nose2rt.rt

[rt]
endpoint = http://127.0.0.1/loader  # Your Testgr service URL
show_errors = True # show POST errors
```
### Launch
```
nose2 -RT -> will launch nose2 with nose2rt plugin.
nose2 -RT -RTE "DEV" -> will launch nose2 and send your environment name as additional info to the Testgr server. 
```

### POST requests examples produced by nose2rt

#### startTestRun
```
{
	"type": "startTestRun",
	"job_id": "07942d9c-03e8-4164-8709-2314119ad60b",
	"tests": {
		"test_method1": "project.folder.test_something.TestSomething.test_method1",
		"test_method2": "project.folder.test_something2.TestSomething2.test_method2"
	},
	"env": "DEV",
	"startTime": "1536775271.8475103"
}
```
#### startTest
```
{
	"type": "startTest",
	"job_id": "07942d9c-03e8-4164-8709-2314119ad60b",
	"test": "project.folder.test_something.TestSomething.test_something",
	"startTime": "1536775300.8666112"
}
```
#### stopTest
```
{
	"type": "stopTest",
	"job_id": "07942d9c-03e8-4164-8709-2314119ad60b",
	"test": "project.folder.test_something.TestSomething.test_something",
	"stopTime": "1536775311.1239314",
	"status": "error",
	"msg": [
          "<class 'AttributeError'>",
          "'NoneType' object has no attribute 'location'",
          "<traceback object at 0x7ffac0a10f89>"
          ]
}
```
#### stopRun
```
{
	"type": "stopTestRun",
	"job_id": "07942d9c-03e8-4164-8709-2314119ad60b",
	"tests_success": "1",
	"tests_errors": "1",
	"tests_failed": "0",
	"tests_skipped": "0",
	"stopTime": "1536775311.141048",
	"timeTaken": "39.294"
}
```      

## Authors

[**Andrey Smirnov**](https://github.com/and-sm)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


