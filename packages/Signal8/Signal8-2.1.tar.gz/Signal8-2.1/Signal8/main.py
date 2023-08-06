import Signal8

env = Signal8.env()
env.reset(options={"problem_name": "disaster_response_0"})
observation, _, terminations, truncations, _ = env.last()
entities = env.unwrapped.get_start_state()
env.step(1)
env.close()