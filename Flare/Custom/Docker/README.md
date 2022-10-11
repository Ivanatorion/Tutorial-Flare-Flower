# Aplicação customizada para o FLARE

Construa a imagem (Aprox. 15GB) com:

```sh
sudo docker build -t custom-flare .
```

E execute o container com:

```sh
sudo docker run -it --network host custom-flare /bin/bash
```

Dentro do container, utilize o script para lançar 4 terminais com o tmux para o servidor, admin e 2 clientes:

```sh
./tmux-script.sh
```

Com o terminal do admin, envie o job com:

```sh
submit_job dist-search
```
