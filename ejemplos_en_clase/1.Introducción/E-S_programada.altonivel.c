#include <fcntl.h>
#include <stdio.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
  char* fuente = "/home/gwolf/vcs/sistemas_operativos/laminas/03-relacion-con-el-hardware.org";
  char* dest = "/tmp/laminas.org";
  FILE* fh_fuente;
  FILE* fh_dest;
  char buf[32];

  fh_fuente = fopen(fuente, "r");
  fh_dest = fopen(dest, "w+");

  while(fgets(buf, 16, fh_fuente) != NULL) {
    fprintf(fh_dest, buf);
  }

  /* printf("Total escrito: %d bytes\n", tot_bytes); */
}
