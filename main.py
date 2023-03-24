from jobs import  *
import os

PATH = os.path.join(os.path.dirname(__file__), 'chromedriver')

if __name__ == '__main__':
    try:
        gmarket.run(PATH)
    except Exception as e:
        print('gmarket error')
        print(type(e))
        print(e)
    finally:
        print('gmarket done')

    try:
        danawa.run(PATH)
    except Exception as e:
        print('danawa error')
        print(type(e))
        print(e)
    finally:
        print('danawa done')


