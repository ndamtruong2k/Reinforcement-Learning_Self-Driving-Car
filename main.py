import os

os.environ['CUDA_VISIBLE_DEVICES'] = ''

import pygame
import logging
import tensorflow as tf

tf.test.is_gpu_available()

from core import learning

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logger = tf.get_logger()
logger.setLevel(logging.ERROR)


if __name__ == '__main__':
    # EVALUATION:
    towns = ['Town01', 'Town02', 'Town03', 'Town04', 'Town05']

    for mode in ['train', 'test']:
        for town in towns:
            for traffic in ['no', 'regular']:
                for num_steps in [512]:
                    print(f'Evaluating [mode={mode}, town={town}, traffic={traffic}, steps={num_steps}]')
                    learning.evaluate(mode, town=town, steps=num_steps, seeds=[42], traffic=traffic)
    exit()
    
    # CURRICULUM LEARNING:
    # -- STAGE-1 --
    stage1 = learning.stage_s1(episodes=500, timesteps=512, batch_size=64, gamma=0.9999, lambda_=0.999, save_every='end',
                               update_frequency=1, policy_lr=3e-4, value_lr=3e-4, dynamics_lr=3e-4,
                               clip_ratio=0.2, entropy_regularization=1.0, seed_regularization=True, load=False,
                               seed=51, polyak=1.0, aug_intensity=0.0, repeat_action=1, load_full=False)
    
    stage1.run2(epochs=100, epoch_offset=0)
    exit()

    # -- STAGE-2 --
    stage2 = learning.stage_s2(episodes=500, timesteps=512, batch_size=64, gamma=0.9999, lambda_=0.999, save_every='end',
                               update_frequency=1, policy_lr=3e-5, value_lr=3e-5, dynamics_lr=3e-4,
                               clip_ratio=0.15, entropy_regularization=2.0, seed_regularization=True,
                               seed=51, polyak=1.0, aug_intensity=0.0, repeat_action=1)

    stage2.run2(epochs=100, epoch_offset=0)
    exit()

    # -- STAGE-3 --
    stage3 = learning.stage_s3(episodes=500, timesteps=512, batch_size=64, gamma=0.9999, lambda_=0.999, save_every='end',
                               update_frequency=1, policy_lr=3e-5, value_lr=3e-5, dynamics_lr=3e-4,
                               clip_ratio=0.125, entropy_regularization=1.0, seed_regularization=True,
                               seed=51, polyak=1.0, aug_intensity=0.0, repeat_action=1)

    stage3.run2(epochs=100, epoch_offset=0)
    exit()

    # EVALUATION:
    towns = ['Town01', 'Town02', 'Town03', 'Town04', 'Town05']

    for mode in ['train', 'test']:
        for town in towns:
            for traffic in ['no', 'regular']:
                for num_steps in [512]:
                    print(f'Evaluating [mode={mode}, town={town}, traffic={traffic}, steps={num_steps}]')
                    learning.evaluate(mode, town=town, steps=num_steps, seeds=[42], traffic=traffic)
    exit()
    pygame.quit()
