import random,string

from django.contrib.auth import get_user_model

User=get_user_model()


class Generator:
    @staticmethod
    def create_code(size):
        return ''.join(random.choice(string.digits) for _ in range(size))
    
    def check_code(self,size):
        code=self.create_code(size)
        checker=User.objects.filter(activation_code=code).exists()

        return code if not checker else self.check_code(size)