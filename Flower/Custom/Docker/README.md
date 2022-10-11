# Aplicação customizada para o Flower

Construa a imagem (Aprox. 2GB) com:

```sh
sudo docker build -t custom-flower .
```

E execute o container com:

```sh
sudo docker run -it --network host custom-flower /bin/bash
```

Dentro do container, utilize o script para lançar 3 terminais com o tmux para o servidor e 2 clientes:

```sh
./tmux-script.sh
```
