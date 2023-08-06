# PyB2f

This python package is used for python webservers that use Blue2Factor

It can be used with both Django and Flask. 

##### To install with pip:

`pip install Blue2Factor`

You may have to install the packages below:

`python3 -m pip install jwt rsa django flask requests`

##### Or on GitHub at [https://github.com/bk89686/PyB2f](https://github.com/bk89686/PyB2f)

### To call in Flask:

```
from Blue2Factor import Authentication

companyId = "COMPANY_ID from https://secure.blue2factor.com"
loginUrl = "LOGIN_URL that was entered at https://secure.blue2factor.com"

b2f = Authentication.Auth()

@app.route('/mytest', methods=['GET', 'POST'])
def myTest():
    if not b2f.authenticateFlaskRequest(request, companyId, loginUrl, privateKeyStr):
        return b2f.redirect
    #do what you would normally do, and set cookies
    response = Main.Sample().showTestPage()
    return response
    
@app.after_request
def setCookie(response):
    return b2f.setB2fCookie(response)
    
    
#If a user signs out call:
	return b2f.flaskSignout(companyId) 

```

### Or using Django

```
from Blue2Factor import Authentication

companyId = "COMPANY_ID from https://secure.blue2factor.com"
loginUrl = "LOGIN_URL that was entered at https://secure.blue2factor.com"

b2f = Authentication.Auth()

def index(request):
	if not b2f.authenticateDjangoRequest(request, companyId, loginUrl, privateKeyStr):
        return b2f.redirect
    #do what you normall do
    template = loader.get_template('sample.html')
    response = HttpResponse(template.render())

@app.after_request
def setCookie(response):
    return b2f.setB2fCookie(response)
    
#If a user signs out call:
	return b2f.djangoSignout(companyId)
```

for questions, please contact us at (607) 238-3522 or help@blue2factor.com