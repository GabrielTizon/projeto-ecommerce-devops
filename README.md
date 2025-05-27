No projeto eu usei pros Dockerfiles, products: Configura o container Node.js para executar a API de produtos. Instala o Express, copia os arquivos e inicia o servidor na porta 3001; orders: Gera a imagem Python para a API de pedidos. Instala Flask, MySQL Connector, Redis e Requests. O aplicativo funciona na porta 3002payments: Prepara um container PHP, copia o index.php e inicia o servidor na porta 3003. 

*O que cada serviço do docker-compose.yml realiza*

products, inicializa a API de produtos, acessível pela porta 3001. 

orders, coloca para rodar a API de pedidos, que depende do banco, Redis e products. Recebe configurações via variáveis e expõe a porta 3002. 

payments, inicializa a API de pagamentos, que depende do serviço orders, rodando na porta 3003. 

db: Banco MySQL com senha root/example, banco ecommerce, porta 3307 (ou 3306), volume para armazenamento persistente. 

redis, executa o Redis, padrão na porta 6379. 

volumes, assegura que os dados do MySQL sejam mantidos mesmo após reiniciar o serviço.
