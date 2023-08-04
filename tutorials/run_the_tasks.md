# Running the tasks
This year's MyoChallenge consists of two independant tracks: Manipulation and locomotion.

In order to create the environments, we can use OpenAI's gym interface, and import myosuite.
It is required to install `myosuite==1.7.0` to run the tasks.

Please note that the rewards given by the environments are NOT the final evaluation metrics, you have to find a good reward function by yourself. We refer to [evalai](https://eval.ai/web/challenges/challenge-page/2105/evaluation) for the evaluation details.

You are also free to change observations, episode length and all kinds of details during training, but during evaluation everything will be fixed to the original environments. Make sure that you can recover your observation vector from the original observations or you cannot run your solution on the evaluation server!
## Manipulation track

This code snippet runs the manipulation track environment with a random agent. We also show how you can render your environment in order to visualize it. You might have to adjust this function in case you are running your code inside a notebook. See this [colab](https://colab.research.google.com/drive/1zFuNLsrmx42vT4oV8RbnEWtkSJ1xajEo)-notebook of the MyoSuite documentation.

``` python
import gym
import myosuite 

env = gym.make('myoChallengeRelocateP1-v0')
for ep in range(5):
    print(f'Episode: {ep} of 5')
    state = env.reset()
    while True:
        action = env.action_space.sample()
        # uncomment if you want to render the task
        # env.mj_render()
        next_state, reward, done, info = env.step(action)
        state = next_state
        if done: 
            break
```

## Locomotion track

In addition to the publicly available task seen below, the locomotion track features an evader during evaluation that is not known during training. Don't be surprised if your evaluation score is slightly lower than your training score.

``` python
import gym
import myosuite 

env = gym.make('myoChallengeChaseTagP1-v0')
for ep in range(5):
    print(f'Episode: {ep} of 5')
    state = env.reset()
    while True:
        action = env.action_space.sample()
        # uncomment if you want to render the task
        # env.mj_render()
        next_state, reward, done, info = env.step(action)
        state = next_state
        if done: 
            break
```



