Auth package is crated for authenticating user for microservices.
It is in beta version and I don't recomd to use it for production until the stable release.

In order to use auth package first install the package by 

pip install auth-package==1.1

then import it 

from auth_package import user, permission

api_key = 'test_api_e56643c8-2311-4e25-991f-03d365243f51'

email = 'test@gmail.com'
first_name = 'test1'
last_name = 'test2'
password = 'password'

for creating user

create_user = user.create_user(email, first_name, last_name, password, api_key)
user_list = user.user_list(api_key)


for authenticating user 

authenticate = user.authenticate_user(email, password, api_key)
print(authenticate)