# Delete servers files metrics.
rm server_*.metrics

# INICIAR SERVIDORES.
echo "STARTING SERVER ON PORT 9097"
python server.py 9097 &
echo "STARTING SERVER ON PORT 9098"
python server.py 9098 &
echo "STARTING SERVER ON PORT 9099"
python server.py 9099 &

