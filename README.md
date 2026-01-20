# Sample Web Service Application For IdentityIQ Labs

> This readme contains steps to setup the sample web service application, and contains ALL the endpoints included with it.
> 

### Setup Steps

1. Run the following commands
    
    ```bash
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv sqlite
    ```
    
2. Clone the repository

   ```bash
   git clone https://github.com/ruglawy/sample-web-service-app.git
   ```
    
4. Install dependencies
    
    ```bash
    pip3 install -r requirements.txt
    ```
    
5. Start the web service
    
    > Make sure you’re in the `webservice_app` directory
    > 
    
    ```bash
    python3 -m uvicorn app.main:app --host 0.0.0.0 --port 9000
    ```
    
6. Test it to ensure it's working
    
    ```bash
    curl -H "X-API-Key: sailpoint-lab-key" http://localhost:9000/api/health
    ```
    
    Expected output:
    
    ```jsx
    {
    	"status":"ok"
    }
    ```
    

### Base URL

```bash
http://localhost:9000/api
```

### Authentication Header

> This header must be added in all the HTTP requests, as it’s used as authentication.
> 

> Without this header, you will get a 400/401 error
> 

```bash
X-API-Key: sailpoint-lab-key
```

### Available Endpoints

- **HEALTH CHECK**
    1. Context URL
        
        ```bash
        /health
        ```
        
    2. HTTP Request Method: **GET**
    3. Sample Body: **NO BODY REQUIRED**
    4. Sample Output with **`200 OK`** Response Code
        
        ```json
        {
        	"status":"ok"
        }
        ```
        

- **RETRIEVE USERS**
    1. Context URL
        
        ```bash
        /users
        ```
        
    2. HTTP Request Method: **GET**
    3. Sample Body: **NO BODY REQUIRED**
    4. Sample Output with **`200 OK`** Response Code
        
        ```bash
        {
            "content": [
                {
                    "id": "57dc8271-59eb-4313-b54d-ddb517af1b5a",
                    "username": "kareem.ramzi",
                    "email": "kareem_ramzi@example.com",
                    "displayName": "Kareem Ramzi",
                    "isActive": true,
                    "groups": [
                        {
                            "id": "4048403e-3db8-4080-abdc-9a7cc8f66980",
                            "name": "EDITOR",
                            "description": "Editors"
                        }
                    ]
                },
                {
                    "id": "dc0eca45-39c3-4556-b747-7b605b0db1ab",
                    "username": "ahmed.mohamed",
                    "email": "ahmed_mohamed@example.com",
                    "displayName": "ahmed.mohamed",
                    "isActive": true,
                    "groups": [
                        {
                            "id": "e3bc3dc6-dfbc-4451-9195-daf9ddab76b0",
                            "name": "USER",
                            "description": "Standard users"
                        }
                    ]
                },
                {
                    "id": "f1260389-3a15-4529-8c7c-c4eaa0cfc4bc",
                    "username": "salma.ahmed",
                    "email": "salma_ahmed@example.com",
                    "displayName": "salma.ahmed",
                    "isActive": false,
                    "groups": []
                }
            ],
            "page": 0,
            "size": 50,
            "totalElements": 3,
            "isLastPage": true
        }
        ```
        

- **RETRIEVE A SINGLE USER**
    1. Context URL
        
        ```bash
        /users/{USER_UUID} 
        
        # Example:
        # /users/57dc8271-59eb-4313-b54d-ddb517af1b5a
        ```
        
    2. HTTP Request Method: **GET**
    3. Sample Body: **NO BODY REQUIRED**
    4. Sample Output with **`200 OK`** Response code
        
        ```bash
        {
            "id": "57dc8271-59eb-4313-b54d-ddb517af1b5a",
            "username": "kareem.ramzi",
            "email": "kareem_ramzi@example.com",
            "displayName": "Kareem Ramzi",
            "isActive": true,
            "groups": [
                {
                    "id": "4048403e-3db8-4080-abdc-9a7cc8f66980",
                    "name": "EDITOR",
                    "description": "Editors"
                }
            ]
        }
        ```
        

- **RETRIEVE ALL GROUPS**
    1. Context URL
        
        ```bash
        /groups
        ```
        
    2. HTTP Request Method: **GET**
    3. Sample Body: **NO BODY REQUIRED**
    4. Sample Output with **`200 OK`** Response Code
        
        ```bash
        [
            {
                "id": "92fd4c92-16a4-44ba-b019-000321184d0f",
                "name": "ADMIN",
                "description": "Administrators"
            },
            {
                "id": "4048403e-3db8-4080-abdc-9a7cc8f66980",
                "name": "EDITOR",
                "description": "Editors"
            },
            {
                "id": "f1909e12-e26a-48fb-83bd-1ed5c8bc999e",
                "name": "SUPER ADMIN",
                "description": "Super administrators"
            },
            {
                "id": "e3bc3dc6-dfbc-4451-9195-daf9ddab76b0",
                "name": "USER",
                "description": "Standard users"
            }
        ]
        ```
        

- **CREATE USER**
    1. Context URL
        
        ```bash
        /users
        ```
        
    2. HTTP Request Method: **POST**
    3. Sample Body
        
        ```bash
        {
            "username": "test.user",
            "email": "test_user@example.com",
            "displayName": "Test User"
        }
        ```
        
    4. Sample Output with **`201 Created`** Response Code
        
        ```bash
        {
            "id": "bebceb28-cb6e-4266-87eb-2f1799f2baae",
            "username": "test.user",
            "email": "test_user@example.com",
            "displayName": "Test User",
            "isActive": true,
            "groups": []
        }
        ```
        

- **ADD USER TO GROUP**
    1. Context URL
        
        ```bash
        /users/{USER_UUID}/groups/{GROUP_UUID}
        
        # Example
        # /users/57dc8271-59eb-4313-b54d-ddb517af1b5a/groups/92fd4c92-16a4-44ba-b019-000321184d0f
        ```
        
    2. HTTP Request Method: **POST**
    3. Sample Body: **NO BODY REQUIRED**
    4. Sample Output with **`204 No Content`** Response Code: **NO BODY RETURNED**

- **REMOVE USER FROM GROUP**
    1. Context URL
        
        ```bash
        /users/{USER_UUID}/groups/{GROUP_UUID}
        
        # Example
        # /users/57dc8271-59eb-4313-b54d-ddb517af1b5a/groups/92fd4c92-16a4-44ba-b019-000321184d0f
        ```
        
    2. HTTP Request Method: **DELETE**
    3. Sample Body: **NO BODY REQUIRED**
    4. Sample Output with **`204 No Content`** Response Code: **NO BODY RETURNED**

- **ENABLE ACCOUNT**
    1. Context URL
        
        ```bash
        /users/{USER_UUID}
        
        # Example
        # /users/57dc8271-59eb-4313-b54d-ddb517af1b5a
        ```
        
    2. HTTP Request Method: **PATCH**
    3. Sample Body
        
        ```json
        {
        	"isActive": true
        }
        ```
        
    4. Sample Output with **`200 OK`** Response Code
        
        ```json
        {
            "id": "57dc8271-59eb-4313-b54d-ddb517af1b5a",
            "username": "kareem.ramzi",
            "email": "kareem_ramzi@example.com",
            "displayName": "Kareem Ramzi",
            "isActive": true,
            "groups": [
                {
                    "id": "4048403e-3db8-4080-abdc-9a7cc8f66980",
                    "name": "EDITOR",
                    "description": "Editors"
                }
            ]
        }
        ```
        

- **DISABLE ACCOUNT**
    1. Context URL
        
        ```bash
        /users/{USER_UUID}
        
        # Example
        # /users/57dc8271-59eb-4313-b54d-ddb517af1b5a
        ```
        
    2. HTTP Request Method: **PATCH**
    3. Sample Body
        
        ```json
        {
        	"isActive": false
        }
        ```
        
    4. Sample Output with **`200 OK`** Response Code
        
        ```json
        {
            "id": "57dc8271-59eb-4313-b54d-ddb517af1b5a",
            "username": "kareem.ramzi",
            "email": "kareem_ramzi@example.com",
            "displayName": "Kareem Ramzi",
            "isActive": false,
            "groups": [
                {
                    "id": "4048403e-3db8-4080-abdc-9a7cc8f66980",
                    "name": "EDITOR",
                    "description": "Editors"
                }
            ]
        }
        ```
        

- **DELETE ACCOUNT**
    1. Context URL
        
        ```bash
        /users/{USER_UUID}
        
        # Example
        # /users/9fcd6f06-8ccd-4570-adf5-106155a950a6
        ```
        
    2. HTTP Request Method: **DELETE**
    3. Sample Body: **NO BODY REQUIRED**
    4. Sample Output with **`204 No Content`** Response Code: **NO BODY RETURNED**
