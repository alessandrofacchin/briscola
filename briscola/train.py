from briscola.envs.game import Table
from briscola import agents


def play_episode(player1: agents.Agent, player2: agents.Agent, verbose: bool = False) -> Table:
    table = Table()
    rewards = {1: [], 2: []}
    while not table.is_terminal_state:
        player_index = table.active_player
        features = table.get_features(player_index)
        if player_index == 1:
            card_index = player1.act(features, table.player_1, table.card_played, table.middle_card)
        elif player_index == 2:
            card_index = player2.act(features, table.player_2, table.card_played, table.middle_card)

        reward = table.play_card(card_index)

        if not table.card_played:
            if verbose:
                print('Winner is player %d:\n\r\tCard played by player 1: %s\n\r\tCard played by player 2: '
                      '%s\n\r\tPoints player 1: %d\n\r\tPoints player 2: %d' % (table.plays[-1][0],
                                                                                table.plays[-1][1].get_name(),
                                                                                table.plays[-1][2].get_name(),
                                                                                table.points[:,0], table.points[:,1]))

            rewards[player_index].append(reward)
            rewards[3 - player_index].append(-reward)
            if table.active_player == 1:
                player1.learn(rewards[table.active_player][-1], table.get_features(player_index))
            else:
                player2.learn(rewards[table.active_player][-1], table.get_features(player_index))
    return table
