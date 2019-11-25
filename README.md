# Pedra Papel Tesoura Com Multi Agentes

## Introducao

Este projeto foi realizado para a matéria paradigmas de programação, ministrada pela Universidade de Brasilia, UnB, campus Gama.
O Objetivo deste projeto é a construção de um sistema baseado no paradigmas de multi agentes, capaz de simular o jogo de pedra, papel tesoura.


## Como executar

Para executar o projeto é necessario a instalacao e configuracao de um servidor XMPP. 
É recomendada a instalaçao do Prosody IM, sendo setado para que o servidor seja levantado no 
"localhost". 

Como instalar o Prosody IM : https://prosody.im/

Outras opções de servidores XMPP : https://xmpp.org/software/servers.html     


Após configurado o servidor basta a instalação da bibliteca Spade

```console
sudo pip3 install spade
```

E finalmente a execussão do programa:

```console
python3 main.py
```