import Signal8

env = Signal8.env()
env.reset(options={"problem_name": "disaster_response_0"})
env.step(1)
observation, reward, termination, truncation, info = env.last()
env.unwrapped.scenario.stop_scripted_obstacles()