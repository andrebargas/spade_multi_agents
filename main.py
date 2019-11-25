import time
from asyncio.base_futures import CancelledError
import os
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


def create_user_player(jogada, judge_jid):
    player_jid = "p_{}@localhost".format("user")
    player_passwd = "secret"

    player = UserPlayerAgent(jogada, judge_jid, player_jid, player_passwd)
    future = player.start(auto_register=True)
    future.result()
    print("UserPlayer iniciado!")

    return player


class UserPlayerAgent(Agent):

    # Inner class para a definicao do comportamento.
    class PlayBehav(OneShotBehaviour):
        async def run(self):
            # print("PlayBehav esta sendo executado!")
            msg = Message(to=self.agent.recv_jid)
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative

            msg.body = "user-" + self.agent.jogada  # Set the message content

            await self.send(msg)
            # print("Jogada foi mandada!")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("UserPlayerAgent foi iniciado")
        b = self.PlayBehav()
        self.add_behaviour(b)

    def __init__(self, jogada, recv_jid, *args, **kwargs):
        self.recv_jid = recv_jid
        self.jogada = jogada
        super().__init__(*args, **kwargs)


class PlayerAgent(Agent):

    # Inner class para a definicao do comportamento.
    class PlayBehav(OneShotBehaviour):
        async def run(self):
            msg = Message(to=self.agent.recv_jid)
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative

            msg.body = self.agent.player_n + "-" + choice(self.agent.items)  # Set the message content

            await self.send(msg)
            # print("Jogada foi mandada!")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        # print("PlayerAgent foi iniciado")
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
                print("Player 2 jogou : {}".format(jogada_2))
            else:
                print("Did not received any message after 10 seconds")
            # stop agent from behaviour

            winner_resp = get_winner(jogada_1, jogada_2)

            print_result(winner_resp)

            await self.agent.stop()

    async def setup(self):
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)


def show_menu():

    print("BEM VINDO AO MULTI JOKEN-PO")
    print("Selecione uma da opcoes ")
    print("1 - Jogar com um agente autonomo ")
    print("2 - Agentes autonomos jogando entre si")
    print("3 - Sair ")


def getJogada():
    while True:git 
        jogada = input("Qual a jogada voce quer fazer ? (pedra, papel ou tesoura) \n")

        if jogada in ["pedra", "papel", "tesoura"]:
            return jogada
        else:
            continue

def do_user_play():
    os.system('cls' if os.name == 'nt' else 'clear')
    judge_jid = "j@localhost"
    judge_passwd = "secret"
    judge_agent = JudgeAgent(judge_jid, judge_passwd)
    future = judge_agent.start(auto_register=True)
    future.result()


    print("Agentes jogando contra usuario : \n")

    jogada = getJogada()
    user = create_user_player(jogada, judge_jid)

    player1 = create_player("2", judge_jid)

    exit()
    while judge_agent.is_alive():
        try:
            time.sleep(2)
            player1.stop()
            user.stop()
            judge_agent.stop()
            exit()
            break
        except KeyboardInterrupt:
            player1.stop()
            user.stop()
            judge_agent.stop()
            break
    quit_spade()



















def do_agents_play():

    os.system('cls' if os.name == 'nt' else 'clear')

    judge_jid = "j@localhost"
    judge_passwd = "secret"
    judge_agent = JudgeAgent(judge_jid, judge_passwd)
    future = judge_agent.start(auto_register=True)
    future.result()



    print("Agentes jogando entre si : \n")

    player1 = create_player("1", judge_jid)
    player2 = create_player("2", judge_jid)




    exit()
    while judge_agent.is_alive():
        try:
            time.sleep(2)
            player1.stop()
            player2.stop()
            judge_agent.stop()
            exit()
            break
        except KeyboardInterrupt:
            player1.stop()
            player2.stop()
            judge_agent.stop()
            break
    quit_spade()


if __name__ == "__main__":

    show_menu()
    opcao = input()

    while opcao != "3":
        if opcao == "1":
            do_user_play()

        elif opcao == "2":

            do_agents_play()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Opcao invalida !!!\n")
            show_menu()
            opcao = input()


