try:
    from .key import *
except:
    pass
from .get_file import TOS

print(TOS)
print()
if input("Do you agree with the Terms of Service? y/n: ") == 'y':
    print('Loading...', end = '\r')
    print()
    from .Analyzer import Analyzer
    from .Blossom import Blossom
    from .Channels import Channels
    from .Chat import Chat
    from .Data import Data
    #from .Functions import Functions
    from .GPTModel import GPTModel
    from .Index import Index
    from .Plots import Plots
    from .Timezone import Timezone
else:
    print("You must agree to the Terms of Service.")