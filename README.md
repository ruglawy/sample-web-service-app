#############################################
This README contains steps to setup the web service application, and contains ALL the endpoints included with it.
#############################################



Steps to run this web service application:

1. Run the following commands:

	- sudo apt update
	- sudo apt install -y python3 python3-pip python3-venv unzip

2. Unzip the web service zip file

	- unzip webservice_app.zip

3. Install dependencies

	- pip3 install -r requirements.txt

4. Start the web service

	- python3 -m uvicorn app.main:app --host 0.0.0.0 --port 9000

5. Test it to ensure it's working

	- curl -H "X-API-Key: sailpoint-lab-key" http://localhost:9000/api/health

	Expected result:
	{"status":"ok"}

#############

Available endpoints:

 
