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

    try:
        danawa_check.run()
    except Exception as e:
        print('danawa_check error')
        print(type(e))
        print(e)
    finally:
        print('danawa_check done')


