import java.util.Scanner;

public class Hola_mundo {
    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);
        System.out.print("Por favor, introduce tu nombre: ");

        String nombre = scanner.nextLine();
        System.out.println("¡Hola, " + nombre + "!");
        scanner.close();
        
    }
}
