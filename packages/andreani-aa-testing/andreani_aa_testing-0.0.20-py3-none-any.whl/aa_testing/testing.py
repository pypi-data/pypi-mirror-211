import time

class Testing():
    def __init__(self, first_function, second_function, dataset):
        self.first_function = first_function
        self.second_function = second_function
        self.dataset = dataset

    def compare_functions(self):
        start_time = time.time()
        result1 = self.first_function(self.dataset)
        end_time = time.time()
        self.time1 = end_time - start_time

        start_time = time.time()
        result2 = self.second_function(self.dataset)
        end_time = time.time()
        self.time2 = end_time - start_time

    def create_response(self):
        json_response = {
            "first_function_time": self.time1,
            "second_function_time": self.time2
        }

        return json_response