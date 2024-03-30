// Programa de asignación de memoria que resuelve solicitudes por primer ajuste.
#include <bits/stdc++.h>

using namespace std;
// Vector que almacena es estado de la memoria
vector < char > memoryUnits(30, '-');
// Variables que ayudan a conocer el nombre que se le asignará al proceso
char initialName = 'A';
int processName = 0;
// Variable que lleva la cuenta de la cantidad de unidades de memoria libres
int freeMemoryUnits = 30;
// Conjunto con el nombre de todos los procesos en ejecución
set < char > processNames;
// Función que imprime la asignación de la memoria
void printMemory() {
    for (int i = 0; i < 30; i++) {
        cout << memoryUnits[i];
    }
    cout << endl;
}
// Función que compacta la memoria
void compactMemory() {
    cout << "*Compactación requerida*" << endl;
    // Se almacena cada proceso de manera contigua
    string memoryUnitsString = "";
    for (int i = 0; i < 30; i++) {
        if (memoryUnits[i] != '-') memoryUnitsString += memoryUnits[i];
    }
    // Se compactan los procesos y se completa con unidades libres
    for (size_t i = 0; i < memoryUnitsString.size(); i++) {
        memoryUnits[i] = memoryUnitsString[i];
    }
    for (int i = memoryUnitsString.size(); i < 30; i++) {
        memoryUnits[i] = '-';
    }
    cout << "Nueva situación:" << endl;
    printMemory();
}
// Función que asigna la cantidad de memoria solicitada por primer ajuste
void assignMemory(int memorySize) {
    // Se confirma que existen suficientes unidades libres
    if (freeMemoryUnits >= memorySize) {
        // Bandera que indicará si se requiere una compactación o no
        bool assigned = false;
        int freeCounter = 0;
        for (int i = 0; i < 30; i++) {
            if (memoryUnits[i] == '-') {
                freeCounter++;
                // Si se encuentra un espacio disponible se asigna la memoria y termina la función iterativa
                if (freeCounter == memorySize) {
                    for (int j = i - memorySize + 1; j <= i; j++) {
                        memoryUnits[j] = (char)(initialName + processName);
                    }
                    processName++;
                    freeMemoryUnits -= memorySize;
                    assigned = true;
                    break;
                }
            } else {
                freeCounter = 0;
            }
        }
        // Si no se realizó la signación se compacta la memoria y repite el proceso
        if (!assigned) {
            compactMemory();
            assignMemory(memorySize);
            return;
        }
        // Se imprime el resultado de la asignación
        processNames.insert((char)(initialName + processName - 1));
        cout << "Asignando a " << (char)(initialName + processName - 1) << ":" << endl;
        printMemory();
    } else {
        cout << "Memoria insuficiente" << endl;
    }
}
// Función que libera el proceso solicitado
void freeMemory(char processName) {
    for (int i = 0; i < 30; i++) {
        if (memoryUnits[i] == processName) {
            memoryUnits[i] = '-';
            freeMemoryUnits++;
        }
    }
    // Se elimina el proceso del conjunto y se imrpime el resultado de la liberación
    processNames.erase(processName);
    cout << "Liberando a " << processName << endl;
    cout << "Asignación actual:" << endl;
    printMemory();
}
// Función principal del programa que libera y asigna memoria por primer ajuste
int main() {
    string input = "0";
    int memorySize;
    string processName;
    cout << "Asignación actual:" << endl;
    printMemory();
    // Ciclo while que se ejecuta mientras se de una entrada valida
    while (input.size() == 1 && (input[0] == '0' || input[0] == '1')) {
        cout << "Asignar(0) o liberar(1) memoria: ";
        cin >> input;
        if (input[0] == '0') {
            cout << "Cantidad de unidades de memoria a asignar: ";
            cin >> memorySize;
            if (memorySize < 2 || memorySize > 15) {
                cout << "Cantidad de unidades inválida" << endl;
                cout << "Un proceso puede especificar que requiere entre 2 y 15 unidades." << endl;
                continue;
            }
            assignMemory(memorySize);
        } else if (input[0] == '1') {
            if (processNames.size() == 0) {
                cout << "No hay procesos en memoria" << endl;
                continue;
            }
            char processName;
            cout << "Nombre del proceso a liberar(";
            // Se imprime el nombre de todos los procesos en memoria
            for (auto it = processNames.begin(); it != processNames.end(); it++) {
                cout << * it;
                if (next(it) != processNames.end()) {
                    cout << "";
                }
            }
            cout << "): ";
            cin >> processName;
            if (processNames.find(processName) == processNames.end()) {
                cout << "Proceso no encontrado" << endl;
                continue;
            }
            freeMemory(processName);
        }
    }
    return 0;
}