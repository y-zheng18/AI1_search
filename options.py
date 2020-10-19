import argparse

def get_args():
    args = argparse.ArgumentParser()
    args.add_argument('--m', type=int, default=3)
    args.add_argument('--n', type=int, default=3)
    args.add_argument('--img_src', type=str, default='./img/src.jpg')
    args.add_argument('--pause_time', type=int, default=100)
    args.add_argument('--random_steps', type=int, default=500)
    return args
