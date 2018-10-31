**Local testing**

For a task with the following program parameters:

![](data:)

"program\_pars" : {

"executable" :
"/home/ucare/uCare\_consumer/ucare\_scheduler/health\_data\_ingestor.py",

"cmd\_args" : \[

{

"vendor" : "fitbit"

},

{

"user\_key" :
"03f9607c3c1ca0a0db94df4455a2925185ead96304bff24dd34731933a9c639c"

},

{

"source\_key" :
"e2348892010ac838a547fbb59282228829de37707519938425fdda632ebab6ec"

},

{

"source\_token" :
"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0UUszOTgiLCJhdWQiOiIyMjdWSFAiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcmFjdCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTA2MjAzNzE0LCJpYXQiOjE1MDYxNzQ5MTR9.tLIu-BJx44csC3X3tC7Hl6MXiIL6nSW3HRQC4xHNBzg"

},

{

"vital\_sign" : "steps"

}

\],

"working\_dir" : "/home/ucare/uCare\_consumer/ucare\_scheduler/",

"timeout" : 30

},

![](data:)

The local test should be:

&gt;\$ cd /home/ucare/uCare\_consumer/ucare\_scheduler/

&gt;\$
/home/ucare/uCare\_consumer/ucare\_scheduler/health\_data\_ingestor.py
\\

--vendor fitbit \\

--user\_key
03f9607c3c1ca0a0db94df4455a2925185ead96304bff24dd34731933a9c639c \\

--source\_key
e2348892010ac838a547fbb59282228829de37707519938425fdda632ebab6ec \\

--source\_token
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0UUszOTgiLCJhdWQiOiIyMjdWSFAiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcmFjdCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTA2MjAzNzE0LCJpYXQiOjE1MDYxNzQ5MTR9.tLIu-BJx44csC3X3tC7Hl6MXiIL6nSW3HRQC4xHNBzg
\\

--vital\_sign steps

\

**Solutions to some common mistakes**

1.  

&gt;\$
/home/ucare/Scflex\_services/data\_pull/package/generic\_datapull/generic\_datapull\_venv/bin/python
some\_program.py --arg1 argument\_1

Alternatively, use a shebang in the program itself. For e.g. the first
line of the python script would be

\#!/home/ucare/Scflex\_services/data\_pull/package/generic\_datapull/generic\_datapull\_venv/bin/python

The python script should be executable (e.g. chmod a+x the\_script.py)
under this set-up.

\

\

