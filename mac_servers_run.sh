export WORK_DIR=pwd

# Delete servers files metrics.
rm server_*.metrics

# INICIAR SERVIDORES.
python3 server.py 9097 &
python3 server.py 9098 &
python3 server.py 9099 &

# PRUEBA PUT, GRUPO 1, RANDOM
# primer argumento indica el algoritmo
# python cliente.py 0 PUT dirx/file2 RRCG1/FILE_220301230356071056 1

# sudo kill -9 $(ps -e | grep python | awk '{print $1}')
