# Run the baselines
This year we provide several baselines:
* Manipulation track and locomotion track baselines with [deprl](https://github.com/martius-lab/depRL), also see the [docs](https://deprl.readthedocs.io/en/latest/myo_baselines.html).
* A reflex-based locomotion controller, see [here](https://myosuite.readthedocs.io/en/latest/tutorials.html#load-myoreflex-baseline).

These baselines will not give you good task performance or win the challenge for you, but they provide a nice starting point.

To run the deprl-baselines, you need to install:

``` bash
pip install deprl
```
Take a look [here](https://deprl.readthedocs.io/en/latest/installation.html) if you run into issues or want to install torch-cpu.
The requirements for the reflex-based baseline are contained in the above link.

## Manipulation Track
This deprl-baseline will try to lift the cube upwards.

``` python
import gym
import myosuite, deprl

env = gym.make('myoChallengeRelocateP1-v0')
policy = deprl.load_baseline(env)

for ep in range(5):
    print(f'Episode: {ep} of 5')
    state = env.reset()
    while True:
        action = policy(state)
        # uncomment if you want to render the task
        # env.mj_render()
        next_state, reward, done, info = env.step(action)
        state = next_state
        if done: 
            break
```

You can also use `policy.noisy_test_step(state)` for actions with Gaussian noise. Your results may vary!

## Locomotion track
This deprl-baseline will try to stand around and slowly move across the quad.
``` python
import gym
import myosuite, deprl

env = gym.make('myoChallengeChaseTagP1-v0')
policy = deprl.load_baseline(env)

for ep in range(5):
    print(f'Episode: {ep} of 5')
    state = env.reset()
    while True:
        action = policy(state)
        # uncomment if you want to render the task
        # env.mj_render()
        next_state, reward, done, info = env.step(action)
        state = next_state
        if done: 
            break
```


