class PrepareTaskRecommendationTrainingDataDTO():
    def __init__(self, json_data):
        self.userList = json_data.get('user_list')


