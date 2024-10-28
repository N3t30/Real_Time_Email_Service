Descrição do Progresso do Projeto "Real Time Email Service"

Durante o desenvolvimento do meu projeto "Real Time Email Service", consegui implementar várias funcionalidades importantes, mesmo enfrentando desafios em algumas áreas. Aqui está um resumo do que foi feito:

Funcionalidades Implementadas:
Autenticação de Usuários :

Criei a funcionalidade de registro de usuários, permitindo que novos usuários se cadastrem na aplicação.
A autenticação foi feita para usar JSON Web Tokens (JWT) como parte do processo de login, garantindo segurança nas requisições.
Painel de Mensagens :

Desenvolvi a interface do painel de mensagens, onde os usuários podem enviar mensagens para outros.
Implementei um formulário que captura o destinatário, título e corpo da mensagem.
Envio de Mensagens :

A lógica para enviar mensagens foi criada, incluindo a validação dos dados recebidos.
Ao enviar uma mensagem, a deveria notificar o destinatário via WebSocket, mas ainda não foi possível implementar totalmente devido à falta de conhecimento em WebSockets.
Tratamento de Erros :

Adicionei verificações para garantir que os campos do formulário não sejam vazios e que o destinatário exista.
Desafios Enfrentados:
JWT e Segurança : Não consegui finalizar a implementação do sistema de autenticação com JWT devido à falta de conhecimento dessa tecnologia. Estou ciente de que isso é fundamental para garantir a segurança da aplicação.
Deploy : Enfrentei dificuldades ao tentar configurar o deploy em uma plataforma de nuvem. Embora tenhamos tentado seguir os tutoriais, não consegui deixar a aplicação acessível via HTTPS.
Aprendizados:
Aprendi a usar Django para o desenvolvimento web e estruturar uma aplicação de mensagens em tempo real.
Explorei o uso de WebSockets e JWT, embora não tenha finalizado essa parte.
Melhorei minhas habilidades em JavaScript para lidar com chamadas assíncronas e manipulação do DOM.
Próximos Passos:
Compreenda melhor como funciona a autenticação JWT e a implementação do WebSocket.
Fazer o deploy da aplicação em uma plataforma de nuvem, garantindo que seja acessível via HTTPS.
