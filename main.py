import time
from spade import quit_spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

from random import choice


def get_winner(jogada_p1, jogada_p2):
    if jogada_p1 == jogada_p2:
        return "Empate!"
    elif (jogada_p1 == "pedra" and jogada_p2 == "tesoura") \
            or (jogada_p1 == "tesoura" and jogada_p2 == "papel") \
            or (jogada_p1 == "papel" and jogada_p2 == "pedra"):

        return "Jogador 1 é o vencedor!"
    else:
        return "Jogador 2 é o vencedor!"


def print_result(result_msg):
    print("\n\n\n")
    print("########### RESULTADO ###########")
    print("#################################")
    print(result_msg)
    print("################################")


def create_player(player_number, judge_jid):
    player_jid = "p_{}@localhost".format(player_number)
    player_passwd = "secret"

    player = PlayerAgent("1", judge_jid, player_jid, player_passwd)
    future = player.start(auto_register=True)
    future.result()
    print("Player {} iniciado!".format(player_number))

    return player


class PlayerAgent(Agent):

    # Inner class para a definicao do comportamento.
    class PlayBehav(OneShotBehaviour):
        async def run(self):
            print("PlayBehav esta sendo executado!")
            msg = Message(to=self.agent.recv_jid)
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative

            msg.body = self.agent.player_n + "-" + choice(self.agent.items)  # Set the message content

            await self.send(msg)
            print("Jogada foi mandada!")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("PlayerAgent, number:", self.player_n, " foi iniciado")
        b = self.PlayBehav()
        self.add_behaviour(b)

    def __init__(self, player_n, recv_jid, *args, **kwargs):
        self.recv_jid = recv_jid
        self.player_n = player_n
        self.items = ["pedra", "papel", "tesoura"]
        super().__init__(*args, **kwargs)


class JudgeAgent(Agent):
    class RecvBehav(OneShotBehaviour):
        async def run(self):
            print("RecvBehav running")

            # Recebendo menagem do primeiro jogador
            msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if msg:
                jogada_1 = msg.body.split("-")[1]
                print("Player 1 jogou : {}".format(jogada_1))
            else:
                print("Did not received any message after 10 seconds")

            # Recebendo mensagem do segundo jogador
            msg = await self.receive(timeout=10)
            if msg:
                jogada_2 = msg.body.split("-")[1]
                print("Player 1 jogou : {}".format(jogada_2))
            else:
                print("Did not received any message after 10 seconds")
            # stop agent from behaviour

            winner_resp = get_winner(jogada_1, jogada_2)

            print_result(winner_resp)

            await self.agent.stop()

    async def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)


if __name__ == "__main__":

    judge_jid = "j@localhost"
    judge_passwd = "secret"
    judge_agent = JudgeAgent(judge_jid, judge_passwd)
    future = judge_agent.start(auto_register=True)
    future.result()
    print("Receiver started")

    player1 = create_player("1", judge_jid)
    player2 = create_player("2", judge_jid)

    while judge_agent.is_alive():
        try:
            time.sleep(1)
            print(".", end="")
        except KeyboardInterrupt:
            player1.stop()
            player2.stop()
            judge_agent.stop()
            break
    print("Agents finished")
    quit_spade()
