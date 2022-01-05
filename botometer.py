import botometer

rapidapi_key = "7f3225ca4bmsh59f9108dbfab953p19c57fjsne3d30427f367" # now it's called rapidapi key
twitter_app_auth = {
    'consumer_key': 'QHfHJKuWsyMVoLOgYTTl1pvm2',
    'consumer_secret': 'GLhitq9fW3wXuKWXvHnHFBw2ghnb2IoenrEoQN6Z5v4TUqq5NV',
    'access_token': '1182512372381962245-Ho4ozk4SBXn3vOXc2PXmdRNlkKrd7R',
    'access_token_secret': '1pZjatSreMpAcYkDFuPdiz1ZlGdKMXKewNO34j269o1E2',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

# Check a single account by screen name
result = bom.check_account('@clayadavis')

# Check a single account by id
#result = bom.check_account(1548959833)

# Check a sequence of accounts
#accounts = ['@clayadavis', '@onurvarol', '@jabawack']
print(result)