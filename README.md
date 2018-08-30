# nose2-rt - Real-time status update plugin via HTTP

Using following plugin you can send HTTP POST requests with test status updates to your API endpoint.

### Installing

Put nose2-rt folder in your nose2/plugins folder.

Find your nose2 config file and configure it somehow as described below.

Example:

```
[unittest]
plugins = nose2.plugins.nose2-rt.rt

[rt]
endpoint = http://127.0.0.1  # Your API endpoint
```
### Launch
```
nose2 -rt
```

### POST requests examples produced by nose2-rt

#### startTestRun
```
{
   "type": "startTestRun",
   "job_id": "2e0a9169-2a01-41fa-b94f-6ac3385935d7",
   "tests": "{
                'test_method1': 'project.folder.test_something.TestSomething', 
                'test_method2': 'project.folder.test_something2.TestSomething2'
             }"
}
```
#### startTest
```
{
  "type": "startTest",
        "job_id": "2e0a9169-2a01-41fa-b94f-6ac3385935d7",
        "test": "project.folder.test_something.TestSomething.test_something",
        "startTime": "1535663071.6408737"
      }
```
#### stopTest
```
{
  "type": "stopTest",
  "job_id": "2e0a9169-2a01-41fa-b94f-6ac3385935d7",
  "test": "project.folder.test_something.TestSomething.test_something",
  "stopTime": "1535663089.4163303",
  "status": "error",
  "msg": [
          "<class 'AttributeError'>",
          "'NoneType' object has no attribute 'location'",
          "<traceback object at 0x7ffac0a10f89>"
        ]
      }
    }
```
#### stopRun
```
{
  "type": "stopTestRun",
  "job_id": "2e0a9169-2a01-41fa-b94f-6ac3385935d7",
  "tests_success": "1",
  "tests_errors": "1",
  "tests_failed": "0",
  "tests_skipped": "0",
  "job_time_taken": "24.380"
}
```      

## Authors

[**Andrey Smirnov**](https://github.com/and-sm)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


