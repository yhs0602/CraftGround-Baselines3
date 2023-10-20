from craftground import craftground
from stable_baselines3 import A2C

from action_wrapper import ActionWrapper, Action
from avoid_damage import AvoidDamageWrapper
from fast_reset import FastResetWrapper
from vision_wrapper import VisionWrapper


def main():
    env = craftground.make(
        env_path="../minecraft_env",
        verbose=True,
        port=8023,
        initialInventoryCommands=[],
        initialPosition=None,  # nullable
        initialMobsCommands=[
            "minecraft:husk ~ ~ ~5 {HandItems:[{Count:1,id:iron_shovel},{}]}",
            # player looks at south (positive Z) when spawn
        ],
        imageSizeX=320,
        imageSizeY=240,
        visibleSizeX=320,
        visibleSizeY=240,
        seed=12345,  # nullable
        allowMobSpawn=False,
        alwaysDay=True,
        alwaysNight=False,
        initialWeather="clear",  # nullable
        isHardCore=False,
        isWorldFlat=True,  # superflat world
        obs_keys=["sound_subtitles"],
        initialExtraCommands=[],
        isHudHidden=False,
        render_action=True,
        render_distance=2,
        simulation_distance=5,
    )
    env = FastResetWrapper(
        ActionWrapper(
            AvoidDamageWrapper(VisionWrapper(env, x_dim=320, y_dim=240)),
            enabled_actions=[Action.FORWARD, Action.BACKWARD],
        )
    )

    model = A2C("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=400)

    vec_env = model.get_env()
    obs = vec_env.reset()
    for i in range(1000):
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, done, info = vec_env.step(action)
        vec_env.render("human")
        # VecEnv resets automatically
        # if done:
        #   obs = vec_env.reset()


if __name__ == "__main__":
    main()
