from RepoInfo import *
from UserProfile import *
from UserEvents import *

if __name__ == '__main__':
    # repo_info_scrapper('pytorch/pytorch')
    # repo_info_scrapper('opencv/opencv')
    # repo_info_scrapper('facebook/react-native')
    # repo_info_scrapper('openai/dall-e')
    # repo_info_scrapper('WongKinYiu/yolov7')
    # repo_info_scrapper('kubernetes/kubernetes')
    # repo_info_scrapper('flutter/flutter')
    # repo_info_scrapper('jenkinsci/jenkins')
    # repo_info_scrapper('ansible/ansible')
    # repo_info_scrapper('apache/predictionio')
    # repo_info_scrapper('microsoft/LightGBM')

    event_logger('shhr3y')

    users = ['ezyang', 'malfet', 'zou3519', 'soumith', 'gchanan', 'jerryzh168', 'pytorchmergebot', 'apaszke', 'suo', 'zdevito', 'peterbell10', 'colesbury', 'Yangqing', 'Chillee', 'rohan-varma', 'smessmer', 'albanD', 'kshitij12345', 'vkuzo', 'ssnl', 'janeyx99', 'zasdfgbnm', 'swolchok', 'pietern', 'seemethere', 'bwasti', 'mrshenli', 'houseroad', 'bddppq', 'ngimel']
    for u in users:
        event_logger(u)
    