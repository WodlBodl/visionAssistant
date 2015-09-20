import requests

# Required headers for requests to Imagga API
headers = {
    'accept': 'application/json',
    'authorization': 'Basic YWNjXzRiNjIzMWMxYzdkZmZlYzoxYzlkNjYzZTUzODQwMzY3MmJiZWFkMTRmYjA1ZGRkZQ=='
    }
# Imagga API url
imaggaUrl = 'http://api.imagga.com/v1/'

'''
This function posts an image to Imagga's /content endpoint. Once uploaded,
an image can be used in the other endpoints.

Image used is the one stored at images/input.jpg

Inputs:
    None
Outputs:
    - contentId, string
'''
def postImage(imgPath):
    urlContent = imaggaUrl + 'content'
    response = requests.post(urlContent, headers=headers, files={'file': open(imgPath, 'rb')})

    contentId = response.json()['uploaded'][0]['id']

    return contentId

'''
This function obtains tags with a confidence greater than 40 percent for the
image at images/input.jpg

Inputs:
    None
Outputs:
    - tags, array, each entry is a dictionary with the following
        keys {'tag', 'confidence'}
'''
def tagImage(imgPath):
    tags = []
    # Obtains the iamge ID
    imgContentId = postImage();

    urlTagging = imaggaUrl + 'tagging'

    querystring = {'content': imgContentId,'version':'2'}

    response = requests.request('GET', urlTagging, headers=headers, params=querystring)

    unfilteredTags = response.json()['results'][0]['tags']

    # Removes the iamge from Imagga once tags are obtained
    deleteUrl = imaggaUrl + 'content/' + imgContentId
    deletedResponse = requests.delete(deleteUrl, headers=headers)

    for tag in unfilteredTags:
        if float(tag['confidence']) > 15:
            tags.append(tag)

    return tags
