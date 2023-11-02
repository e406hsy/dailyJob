from jobs import *

if __name__ == '__main__':
    try:
        gmarket.run()
    except Exception as e:
        print('gmarket error')
        print(type(e))
        print(e)
    finally:
        print('gmarket done')

    try:
        danawa.run()
    except Exception as e:
        print('danawa error')
        print(type(e))
        print(e)
    finally:
        print('danawa done')


