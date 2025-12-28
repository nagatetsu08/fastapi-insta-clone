# 以下のようにすると、メッセージを変えたいときだけthrowするときにメッセージ指定すればいい
class PostNotFoundException(Exception): 
    def __init__(self, message="Post not found"):
        self.message = message
        super().__init__(self.message)

class UnauthorizedException(Exception):
    def __init__(self, message="Unauthorized"):
        self.message = message
        super().__init__(self.message)