from dishpill.envs.registration import load_env_plugins as _load_env_plugins
from dishpill.envs.registration import make, register, registry, spec

# Hook to load plugins from entry points
_load_env_plugins()

register(
    id="Pong-v0",
    entry_point="dishpill.envs.dishgames.pong:Pong",
    max_episode_steps=1600,
    reward_threshold=300,
)


