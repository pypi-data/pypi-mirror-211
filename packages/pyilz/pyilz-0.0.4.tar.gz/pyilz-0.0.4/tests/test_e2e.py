from pyilz import get_token, get_game_state,parse_land,get_timers
token = get_token.get_token()
game_state = get_game_state.get_game_state(token)
land = parse_land.parse_land(game_state)
land0 = land[0]
timers = get_timers.get_timers(land0)
print(timers)