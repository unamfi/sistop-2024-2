package sachhe.tareas_sistop;
import java.util.Scanner;
/**
 *
 * @author SamChong
 */
public class Tareas_sistop {

    static char[] memoria;
    static int tamMemoria = 30;
    
    public static void main(String[] args) {
        
        Scanner scan = new Scanner(System.in);
        memoria = new char[tamMemoria];
        inicializarMemoria();
        
        while(true){
            System.out.println("Estado memoria: ");
            mapaMemoria();
            System.out.print("(0) para asignar / (1) para liberar / (cualquier otro numero) salir: ");
            int opcion = scan.nextInt();
            
            if(opcion == 0){
                System.out.print("Nuevo proceso, elegir [a-z]: ");
                char proceso = scan.next().charAt(0);
                asignarMemoria(proceso);
            }else if(opcion == 1){
                System.out.print("Proceso a liberar, escoger el proceso [a-z]: ");
                char proceso = scan.next().charAt(0);
                liberarMemoria(proceso);
            }else{
                System.out.println("Hasta luego");
                break;
            }
        }
    }
    
    static void inicializarMemoria(){
        for(int i = 0; i < tamMemoria; i++){
            memoria[i] = '-';
        }
    }
    
    static void mapaMemoria(){
        for(char c: memoria){
            System.out.print(c);
        }
        System.out.println();
    }
    
    static void compactarMemoria(){
        char[] memoriaNueva = new char[tamMemoria];
        int indice = 0;
        for(int i = 0; i < tamMemoria; i++){
            if(memoria[i] != '-'){
                memoriaNueva[indice] = memoria[i];
                indice++;
            }
        }
        memoria = memoriaNueva;
        System.out.println("Mapa de memoria: ");
        mapaMemoria();
    }
    
    static void asignarMemoria(char proceso){
        Scanner scan = new Scanner(System.in);
        System.out.println("Requiero entre 2 y 15 unidades: ");
        int unidadesMemoria = scan.nextInt();
        
        int inicio = -1;
        int contador = 0;
        
        for(int i = 0; i < tamMemoria; i++){
            if(memoria[i] == '-'){
                if(inicio == -1){
                    inicio = i;
                }
                contador++;
                if(contador == unidadesMemoria){
                    for(int j = inicio; j < inicio + unidadesMemoria; j++){
                        memoria[j] = proceso;
                    }
                    System.out.println("Nueva asignacion: ");
                    mapaMemoria();
                    return;  
                  }
                }else{
                    inicio = -1;
                    contador = 0;
                }
            }
            System.out.println("Se requiere compactar");
            compactarMemoria();
            asignarMemoria(proceso);
     }    
    
    static void liberarMemoria(char proceso){
        for(int i = 0; i < tamMemoria; i++){
            if(memoria[i] == proceso){
                memoria[i] = '-';
            }
        }
        System.out.println("Mapa actual: ");
        mapaMemoria();
    }
}
