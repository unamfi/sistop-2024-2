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
        
       
    }
    
    /*Esta funcion inicializa la memoria de 30 unidades, con -*/
    static void inicializarMemoria(){
        for(int i = 0; i < tamMemoria; i++){
            memoria[i] = '-';
        }
    }
    
    /*Este metodo muestra el estado de la memoria*/
    static void mapaMemoria(){
        for(char c: memoria){
            System.out.print(c);
        }
        System.out.println();
    }
    
}
