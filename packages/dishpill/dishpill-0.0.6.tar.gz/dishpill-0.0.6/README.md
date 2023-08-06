

## Installation

To install the base dishpill library, use `pip install dishpill[all]` to install all dependencies.

## API

Inspired by Gym library. 
Creating environment instances and interacting with them is very simple- here's an example using the "CartPole-v1" environment:

```python
import dishpill
env = dishpill.make('Pong-v0')
env.reset()
for _ in range(1000):
    observation, reward, done, info = env.step(env.action_space.sample()) # take a random action
    env.render()
env.close()
```
