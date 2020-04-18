import gym
import numpy as np

env = gym.make('MountainCar-v0')

done = False
LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPISODES = 25000
SHOW_EVERY = 2000

epsilon = 0.5
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES // len(env.observation_space.high)
epsilon_decay_value = epsilon / (END_EPSILON_DECAYING - START_EPSILON_DECAYING)

print(env.observation_space.high)
print(env.observation_space.low)
print(env.action_space.n)

DISCRETE_OS_SIZE = [20, 20]
discrete_os_win_size = (env.observation_space.high - env.observation_space.low) / DISCRETE_OS_SIZE

q_tab = np.random.uniform(low=-2, high=0, size=(DISCRETE_OS_SIZE + [env.action_space.n]))
print(q_tab.shape)
print(q_tab)

def get_discrete_state(state):
    discrete_state = (state - env.observation_space.low)/discrete_os_win_size
    return tuple(discrete_state.astype(np.int))


for episode in range(EPISODES):
    if episode % SHOW_EVERY == 0:
        print(episode)
        render = True
    else:
        render = False

    discrete_state = get_discrete_state(env.reset())
    done = False
    while not done:
        if np.random.random() > epsilon:
            action = np.argmax(q_tab[discrete_state])
        else:
            action = np.random.randint(0, env.action_space.n)
        new_state, reward, done, _ = env.step(action)
        new_discrete_state = get_discrete_state(new_state)

        # print(reward, new_state)
        if render:
            env.render()
        if not done:
            max_future_q = np.max(q_tab[new_discrete_state])
            current_q = q_tab[discrete_state + (action, )]

            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            q_tab[discrete_state + (action, )] = new_q
        elif new_state[0] >= env.goal_position:
            print(f'Accomplished on episode: {episode}')
            q_tab[discrete_state + (action, )] = 0

        discrete_state = new_discrete_state

        if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
            epsilon -= epsilon_decay_value


env.close()