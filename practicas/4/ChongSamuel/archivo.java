package ChongSamuel;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class archivo {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        List<String> datos = new ArrayList<>();

        // Solicitar al usuario que ingrese algunos datos
        System.out.println("Por favor, ingrese algunos datos (ingrese una línea vacía para finalizar):");
        while (true) {
            String entrada = scanner.nextLine();
            if (!entrada.isEmpty()) {
                datos.add(entrada);
            } else {
                break;
            }
        }
        scanner.close();

        // Escribir los datos en un archivo de texto
        String nombreArchivo = "datos.txt";
        try (FileWriter escritor = new FileWriter(nombreArchivo)) {
            for (String dato : datos) {
                escritor.write(dato + "\n");
            }
            System.out.println("Los datos se han guardado en el archivo '" + nombreArchivo + "'.");
        } catch (IOException e) {
            System.out.println("Error al escribir en el archivo: " + e.getMessage());
        }
    }
}
