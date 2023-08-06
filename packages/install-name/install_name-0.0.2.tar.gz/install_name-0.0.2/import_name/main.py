
from .fe.fe import cols_fea
from .utils.utils import show_info

def main():
    show_info()
    print('main()')
    print(cols_fea, __name__)

def main_func():
    print('main_func')

if __name__ == '__main__':
   print('inside, __main__')
