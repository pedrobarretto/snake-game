import socket #importa modulo socket

hostname = socket.gethostname()
TCP_IP = socket.gethostbyname(hostname) # endereço IP do servidor 
TCP_PORTA = 24000      # porta disponibilizada pelo servidor
TAMANHO_BUFFER = 1024

msg = ''
while msg != 'quit':
  msg  = input("Digite sua mensagem para o servidor: ")
  # Criação de socket TCP do cliente
  print('1')
  cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print('2')
  # Conecta ao servidor em IP e porta especifica 
  cliente.connect((TCP_IP, TCP_PORTA))
  print('3')
  # envia mensagem para servidor 
  cliente.send(msg.encode('UTF-8'))
  print('4')
  # recebe dados do servidor 
  data, addr = cliente.recvfrom(1024)

  print ("received data:", data)

# fecha conexão com servidor
cliente.close()

# MENSAGEM  = input("Digite sua mensagem para o servidor: ")

# # Criação de socket TCP do cliente
# cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # Conecta ao servidor em IP e porta especifica 
# cliente.connect((TCP_IP, TCP_PORTA))

# # envia mensagem para servidor 
# cliente.send(MENSAGEM.encode('UTF-8'))

# # recebe dados do servidor 
# data, addr = cliente.recvfrom(1024)

# # fecha conexão com servidor
# cliente.close()

# print ("received data:", data)
