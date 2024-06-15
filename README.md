Fancode Assignment
=====

## Scope Of The Assingment

Task : To Automate the Below Scenario.
Scenario :- All the users of City `FanCode` should have more than half of their todos task completed.
Given User has the todo tasks
And User belongs to the city FanCode
Then User Completed task percentage should be greater than 50%

Note :-
- You can use any language to write api automation/Framework.
- Fancode City can be identified by lat between ( -40 to 5) and long between ( 5 to 100) in users api

## Requirements
- Python 3.x
- requirement.txt library (`python3 -m pip install -r requirements.txt`)

### Resources(APIs) :- Endpoint http://jsonplaceholder.typicode.com/ 
[/todos](http://jsonplaceholder.typicode.com/)
[/posts](http://jsonplaceholder.typicode.com/)
[/comments](http://jsonplaceholder.typicode.com/)
[/albums](http://jsonplaceholder.typicode.com/)
[/photos](http://jsonplaceholder.typicode.com/)
[/users](http://jsonplaceholder.typicode.com/)



## Script Overview
The main script, `fancodecities.py`, automates the scenario as follows:
- Python script to automate testing the scenario.
- The script fetches users and todos from the JSONPlaceholder API.
- Calculates the completed task percentage for each user.
- Checks if the completed task percentage for FanCode users is greater than 50%.
- Outputs the result of the test.
- Output can be shown in json or tabular format.
- NOTE:- For Tabular and Json format selected user data is supported and 
         only completed and total tasks will be shown.

## Installation
1. Clone the repository.
```bash
git clone https://github.com/kewalpithadia/FancodeAssignment.git
cd fancode-todos-automation
````

## Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

## How To Run The Script
- Steps
```bash
python3 fancodecities.py endpoint=<somevalue> latrange=<latrange_value> 
                         lngrange=<lngrange_value> format=<format_value>
```
Replace <endpoint_value>, <latrange_value>, <lngrange_value>, and \
<format_value> with appropriate values as described below:
## Supported Arguments
- endpoint (Optional): API endpoint to fetch data. 
  `Default is http://jsonplaceholder.typicode.com/.`
### Example
```bash
python3 fancodecities.py endpoint=http://jsonplaceholder.typicode.com/
```
- latrange (Optional): Latitude range for FanCode cities. Should be a comma-separated string of two numbers 
                       where the first is less than the second.
### Example
```bash
python3 fancodecities.py latrange=-40,5
```

- lngrange (Optional): Longitude range for FanCode cities. Should be a comma-separated string of two numbers 
                       where the first is less than the second.
### Example
```bash
python3 fancodecities.py lngrange=5,100
```

- format(Optional): Output format. Supports `json` or `table`.
### Example
```bash
python3 fancodecities.py format=table
```

## Output Format Details
- If no format is specified or if an unsupported format is provided, the script defaults to displaying complete user data for those who have completed more than or equal to 50% of their tasks.
- For json or table formats, customize the displayed user data keys by editing columns.cfg under the [keys][userkeys] section.
### Example columns.cfg:
```cfg
[keys]
userkeys=id,name,email,address.geo.lat,address.geo.lng,company
```
Note:
- `userkeys` is a comma seperated string which keys that are present in user data. Also you can specify child key by seperating based on `.` as mentioned in above example `address.geo.lat`.
- Ensure keys specified in columns.cfg are valid and exist in the user data structure.
Incorrect keys will be mentioned in the output.
- If no keys are specified in userkeys. All data of Users will be displayed.

## Example
```bash
python3 fancodecities.py endpoint=http://jsonplaceholder.typicode.com/ latrange=-40,5 lngrange=5,100 format=table
```
This command fetches data from the specified endpoint, filters users from FanCode cities based on latitude and longitude ranges, formats the output as a table, and displays users who have completed more than 50% of their todos tasks. With only those key mentioned in columns.cfg.