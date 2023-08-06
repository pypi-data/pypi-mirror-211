
# Key Auth

Authentication Tool for Authenticating Users, HWIDs and Licenses to keep your Code secure from malicious activities.




## Installation

Install keyauth-tech with pip

```bash
  pip install keyauth-tech
```
    
## Usage/Examples

```python
from keyauth import KeyAuth 

authenticator = KeyAuth(app_id="")  # Replace with your actual app_id

if authenticator.authenticate():
    print("Authentication successful!")
else:
    print("Authentication failed.")

```


## Support

For support, email keyauthtech@gmail.com or join our Slack channel.

