#include <fcntl.h>
#include <stdio.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
  char* fuente = "/home/gwolf/vcs/sistemas_operativos/laminas/03-relacion-con-el-hardware.org";
  char* dest = "/tmp/laminas.org";
  int fh_fuente, fh_dest, num_bytes, tot_bytes;
  char buf[32];

  if ((fh_fuente = open(fuente, O_RDONLY)) == -1) {
    perror("Error abriendo archivo fuente");
    exit(1);
  }
  if ((fh_dest = open(dest, O_WRONLY | O_CREAT | O_TRUNC,
		      S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH)) == -1) {
    perror("Error abriendo archivo destino");
    exit(1);
  }

  /* printf("El FH fuente es %d, el FH destino es %d\n", fh_fuente, fh_dest); */
  tot_bytes = 0;
  while ((num_bytes = read(fh_fuente, buf, 16)) > 0) {
    tot_bytes += num_bytes;
    write(fh_dest, buf, num_bytes);
  }
  if (num_bytes == -1 && tot_bytes==0) {
    perror("Error leyendo? (num_bytes == -1, tot_bytes == 0)\n");
    exit(1);
  }
  /* printf("Total escrito: %d bytes\n", tot_bytes); */
  exit(0);
}
