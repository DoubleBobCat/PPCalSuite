g++ -c ITOL_config_gene.cpp
g++ -shared -fPIC -o parallel_calculate.dll ITOL_config_gene.o
del ITOL_config_gene.o