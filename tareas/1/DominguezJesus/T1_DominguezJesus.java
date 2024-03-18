// Alumno: Domínguez Chávez Jesús Abner
// Tarea 1 - Asignación de Memoria con Primer Ajuste
// Materia: Sistemas Operativos
// Profesor: Gunnar Eyal Wolf Iszaevich

import java.util.ArrayList;
import java.util.List;

class BloquedeMemoria {
    int id;
    int size;
    boolean allocated;

    public BloquedeMemoria(int id, int size, boolean allocated) {
        this.id = id;
        this.size = size;
        this.allocated = allocated;
    }
}

public class AsignaciondePrimerAjuste {
    List<BloquedeMemoria> memoria;

    public AsignaciondePrimerAjuste(int size) {
        memoria = new ArrayList<>();
        memoria.add(new BloquedeMemoria((int)(Math.random()*30+1), size, false)); // Genera un número aleatorio para el id de cada bloque de memoria
    }

    public int AsignarMemoria(int processSize) {
        for (BloquedeMemoria bloque : memoria) {
            if (!bloque.allocated && bloque.size >= processSize) {
                bloque.allocated = true;
                if (bloque.size > processSize) {
                    memoria.add(memoria.indexOf(bloque) + 1, new BloquedeMemoria(bloque.id + 1, bloque.size - processSize, false));
                    bloque.size = processSize;
                }
                return bloque.id;
            }
        }
        return -1; // -1 indica que la memoria se encuentra llena y no fue posible asignar memoria
    }

    public void deAsignarMemoria(int id) {
        for (BloquedeMemoria bloque : memoria) {
            if (bloque.id == id) {
                bloque.allocated = false;
                FusionarBloques();
                return;
            }
        }
    }

    private void FusionarBloques() {
        for (int i = 0; i < memoria.size() - 1; i++) {
            BloquedeMemoria current = memoria.get(i);
            BloquedeMemoria next = memoria.get(i + 1);
            if (!current.allocated && !next.allocated) {
                current.size += next.size;
                memoria.remove(next);
                i--; // Ajusta el índice debido a la eliminación de un bloque
            }
        }
    }

    public static void main(String[] args) {
        AsignaciondePrimerAjuste memoryAllocation = new AsignaciondePrimerAjuste(30);

        int processId1 = memoryAllocation.AsignarMemoria(2);
        int processId2 = memoryAllocation.AsignarMemoria(10);
        int processId3 = memoryAllocation.AsignarMemoria(10);
        int processId4 = memoryAllocation.AsignarMemoria(5);
        int processId5 = memoryAllocation.AsignarMemoria(3);
        

        System.out.println("ASIGNACIÓN MEDIANTE PRIMER AJUSTE");
        System.out.println("MAPA DE MEMORIA");
        System.out.println("Proceso 1 asignado a bloque de memoria con ID: " + processId1);
        System.out.println("Proceso 2 asignado a bloque de memoria con ID: " + processId2);
        System.out.println("Proceso 3 asignado a bloque de memoria con ID: " + processId3);
        System.out.println("Proceso 4 asignado a bloque de memoria con ID: " + processId4);
        System.out.println("Proceso 5 asignado a bloque de memoria con ID: " + processId5);

        System.out.println("Desasignando Proceso 2...");
        
        memoryAllocation.deAsignarMemoria(processId2);

        System.out.println("Desasignado el bloque de memoria del proceso 2 con ID: " + processId2);

        System.out.println("Asignando Proceso 6...");

        int processId6 = memoryAllocation.AsignarMemoria(4);

        System.out.println("Proceso 6 asignado a bloque de memoria con ID: " + processId6);
    }
}
