# Testing PyPI Upload after pip install
import thwInfoTabs 



print(dir(thwInfoTabs))

# initialize = thw.THW()

API_URLs = ['https://hashnode.com/api/feed/tag/thw-cloud-computing',
            'https://hashnode.com/api/feed/tag/thw-mobile-apps',
            'https://hashnode.com/api/feed/tag/thw-web3',
            'https://hashnode.com/api/feed/tag/thw-web-apps'
            
            ]


for idx, url in enumerate(API_URLs):
    print(f"API {idx} ; Counter")
    count = thwInfoTabs.THW(url).count()
       

def summarizer():
    for idx, url in enumerate(API_URLs):
        print(f"API {idx} ; Summary")
        summary = thw.THW(url).all_posts()
        return summary
    
# print(counter())
# print(summarizer())
        