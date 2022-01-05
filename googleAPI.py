import requests
import json
def get_recommendation(poi , destination):
    params = {
    'access_key': '888ff2c5161fd89ee128eb7411107a84',
    'query': poi + ' in ' + destination
    }

    api_result = requests.get('http://api.serpstack.com/search', params)

    api_response = api_result.json()
    print(api_response)
    if "top_carousel" in api_response.keys():
        return api_response['top_carousel']['results'] , api_response['organic_results']
    elif "local_results" in api_response.keys():
        return api_response['local_results'] , api_response['organic_results']
    else:
        return None , api_response['organic_results']
if __name__ == "__main__":
    get_recommendation("ba" , "a")