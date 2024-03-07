package sistemasoperativos;
import java.util.Scanner;

public class Saludo{
    public static void main(String[] args) {
        System.out.println("Hola mundo");
        Scanner scanner = new Scanner(System.in);
        System.out.print("Por favor ingresa tu nombre: ");
        String nombre = scanner.nextLine();
        System.out.println("Hola " + nombre + "! Bienvenido al programa de saludo.");
        scanner.close();
    }
}

