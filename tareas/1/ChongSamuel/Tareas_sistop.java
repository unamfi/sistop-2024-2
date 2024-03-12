package sachhe.tareas_sistop;
import java.util.Scanner;
/**
 *
 * @author SamChong
 */
public class Tareas_sistop {

    static char[] memoria;
    static int tamMemoria = 30;
    
    /* Funcion principal del programa */
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
    
    /* Este método inicializa la memoria de 30 unidades con - */
    static void inicializarMemoria(){
        for(int i = 0; i < tamMemoria; i++){
            memoria[i] = '-';
        }
    }
    
    /* Este método muestra el mapa de la memoria */
    static void mapaMemoria(){
        for(char c: memoria){
            System.out.print(c);
        }
        System.out.println();
    }
    
    /* Método encargado de compactar la memoria */
    static void compactarMemoria(){
        char[] memoriaNueva = new char[tamMemoria]; 
        int indice = 0;

        for(int i = 0; i < tamMemoria; i++){
            if(memoria[i] != '-'){
                memoriaNueva[indice] = memoria[i]; //los procesos se van moviendo, compactando la memoria que se refeja del lado derecho
                indice++;
            }
        }
        memoria = memoriaNueva;

        for(int i = indice; i < tamMemoria; i++){
            memoria[i] = '-';       //Se ve la memoria compactada del lado izquierdo
        }
        System.out.println("Mapa actualizado: ");
        mapaMemoria();
    }
    
    /* Este metodo asigna la memoria a los procesos segun las unidades necesarias; siguiendo el peor ajuste */
    static void asignarMemoria(char proceso){
        Scanner scan = new Scanner(System.in);
        System.out.println("Requiero entre 2 y 15 unidades: ");
        int unidadesMemoria = scan.nextInt();
        
        int inicio = -1;
        int contador = 0;
        
        for(int i = 0; i < tamMemoria; i++){
            if(memoria[i] == '-'){
                if(inicio == -1){       //Se recorre el arreglo
                    inicio = i; 
                }
                contador++;
                if(contador == unidadesMemoria){
                    for(int j = inicio; j < inicio + unidadesMemoria; j++){
                        memoria[j] = proceso;       //se asgina el proceso [a-z]
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
            System.out.println("Volver a ingresar las unidades del proceso");
            asignarMemoria(proceso);
     }    
    
     /* Metodo para liberar memoria */
    static void liberarMemoria(char proceso){
        for(int i = 0; i < tamMemoria; i++){
            if(memoria[i] == proceso){
                memoria[i] = '-';       //Segun el proceso que libera memoria, se reemplaza con -
            }
        }
        System.out.println("Mapa actual: ");
        mapaMemoria();
    }
}
