export WORK_DIR=pwd

# CREAR ARCHIVOS GRUPO 1
rm -rf G1_FILES
python file_gen.py 0 100 G1_FILES
# CREAR ARCHIVOS GRUPO 2
rm -rf G2_FILES
python file_gen.py 1 100 G2_FILES
# CREAR ARCHIVOS GRUPO 3
rm -rf G3_FILES
python file_gen.py 2 100 G3_FILES
