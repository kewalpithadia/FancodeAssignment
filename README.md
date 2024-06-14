Fancode Assignment
=====

## Scope Of The Assingment
```
Task : To Automate the Below Scenario.
Scenario :- All the users of City `FanCode` should have more than half of their todos task completed.
Given User has the todo tasks
And User belongs to the city FanCode
Then User Completed task percentage should be greater than 50%

Note :-
- You can use any language to write api automation/Framework.
- Fancode City can be identified by lat between ( -40 to 5) and long between ( 5 to 100) in users api
```
### Resources(APIs) :- Endpoint http://jsonplaceholder.typicode.com/ 
[/todos](http://jsonplaceholder.typicode.com/)
[/posts](http://jsonplaceholder.typicode.com/)
[/comments](http://jsonplaceholder.typicode.com/)
[/albums](http://jsonplaceholder.typicode.com/)
[/photos](http://jsonplaceholder.typicode.com/)
[/users](http://jsonplaceholder.typicode.com/)

## Requirements
- Python 3.x
- requirement.txt library (`python3 -m pip install -r requirements.txt`)

## Script Description
- `fancodecities.py` Python script to automate testing the scenario.
    - The script fetches users and todos from the JSONPlaceholder API.
    - Calculates the completed task percentage for each user.
    - Checks if the completed task percentage for FanCode users is greater than 50%.
    - Outputs the result of the test.
    - Output can be shown in json or tabular format.

## How To Run The Script
- Steps
```
python3 fancodecities.py endpoint=<somevalue> latrange=-40,5 
                         lngrange=5,100 format=table

Supported Arguments
1. endpoint (Optional)
2. latrange (Optional)
3. lngrange (Optional) 
4. format   (Optional)
```
- Information On Arguments
```
endpoint=<somevalue> :- 
This is the endpoint for the api resources. 
(Default Value Is http://jsonplaceholder.typicode.com/)
Example python3 fancodecities.py endpoint=http://jsonplaceholder.typicode.com/

latrange=<somevalue> :-
This is a comma seperated string of 2 Numbers. Number One < Number 2
Example python3 fancodecities.py latrange=-40,5 
(Here -40,5 Denotes the latitude range of a city)
Note:- If Number One > Number Two Script Will Exit with the reason. 
       No Proper Range Provided.

lngrange=<somevalue> :-
This is a comma seperated string of 2 Numbers. Number One < Number 2
Example python3 fancodecities.py lngrange=5,100 
(Here 5,100 Denotes the longotude range of a city)
Note:- If Number One > Number Two Script Will Exit with the reason. 
       No Proper Range Provided.

format=<json/table> :-
This Param supports only 2 input values json or table.
1. If format is given as an argument with value in [json, table].
      You have to mention all the keys of user data 
      you want to see in output in columns.cfg file.
      Example of columns.cfg
      [keys]
      userkeys=id,name,email,address.geo.lat,address.geo.lng,company
      Output will be Selected data for all the user who have have completed
      more than or equal to 50% of their task.
      Note :- userkeys is a comma seperated keys that is part of userdata. 
      If wrong key is provided that will be mentioned in the output.

2. If format is not given as an argument or format value is not in [json, table]. 
      Output will be complete data for all the user who have have completed
      more than or equal to 50% of their task. 
```