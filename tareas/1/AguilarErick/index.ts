import { FirstFitAllocator } from "./controllers/FirstFitAllocator";
import { MemoryManager } from "./controllers/MemoryManager";
import { select, input } from "@inquirer/prompts";
import { BestFitAllocator } from "./controllers/BestFitAllocator";
import { WorstFitAllocator } from "./controllers/WorstFitAllocator";
import { ShowTheCurrentMemory } from "./view/ShowTheCurrentMemory";
import { GlobalConfigurations } from "./GlobalConfigurations";
import { Process } from "./models/Process";
async function selectAlgorithm(memoryManager: MemoryManager) {
  let algoritmo = await select({
    message: "Escoja un algoritmo de asignación de memoria:",
    choices: [
      { name: "First Fit", value: "First Fit" },
      { name: "Best Fit", value: "Best Fit" },
      { name: "Worst Fit", value: "Worst Fit" },
    ],
    default: "First Fit",
  });
  switch (algoritmo) {
    case "First Fit":
      memoryManager.changeAllocationStrategy(new FirstFitAllocator());
      break;
    case "Best Fit":
      memoryManager.changeAllocationStrategy(new BestFitAllocator());
      break;
    case "Worst Fit":
      memoryManager.changeAllocationStrategy(new WorstFitAllocator());
      break;
    default:
      throw new Error("Algoritmo no soportado");
  }
  return algoritmo;
}
async function main() {
  const memoryManager = MemoryManager.getInstance();
  const showMemory = new ShowTheCurrentMemory(memoryManager);
  let algoritmo = await selectAlgorithm(memoryManager);

  while (true) {
    console.log("Algoritmo de asignación: " + algoritmo);
    showMemory.show();

    const action = await select({
      message: "Seleccione una acción:",
      choices: [
        { name: "Agregar proceso", value: "0" },
        { name: "Eliminar proceso", value: "1" },
        { name: "Cambiar algoritmo", value: "2" },
        { name: "Salir", value: "3" },
      ],
      default: "0",
    });
    switch (action) {
      case "0":
        const pid = memoryManager.getNewPid();
        const size = await input({
          message: "Nuevo proceso (" + pid + "):",
          default: "1",
          validate(value) {
            if (!/^\d+$/.test(value))
              return "Ingrese un número entero positivo";
            const { MAX_PROCESS_SIZE } =
              GlobalConfigurations.getConfigurations();
            if (parseInt(value) > MAX_PROCESS_SIZE)
              return (
                "El tamaño del proceso no puede ser mayor a " + MAX_PROCESS_SIZE
              );
            if (parseInt(value) < 1)
              return "El tamaño del proceso no puede ser menor a 1";
            return true;
          },
        });
        const newProcess = new Process(pid);
        const { state } = memoryManager.insertProcess(
          newProcess,
          parseInt(size)
        );
        if (state !== "failed") break;
        console.log(
          "Requiero asignar " +
            size +
            " unidades, sólo tengo " +
            memoryManager.getMaxFreeContiguousMemorySize() +
            " consecutivas disponibles"
        );
        memoryManager.compactMemory();
        showMemory.show("Nueva situación tras compactar:");
        const { state: secondState } = memoryManager.insertProcess(
          newProcess,
          parseInt(size)
        );
        if(secondState !== "failed"){
          showMemory.show("Asignando " + pid + ":");
        }
        if(secondState === "failed"){
          console.log("No hay suficiente memoria para asignar el proceso")
        }
        break;
      case "1":
        const pids = memoryManager.getPids();
        if (pids.length === 0) {
          console.log("No hay procesos para eliminar");
          break;
        }
        const pidToDelete = await select({
          message: "Proceso a eliminar:",
          choices: pids,
        });
        memoryManager.deleteProcess(new Process(pidToDelete));
        break;
      case "2":
        algoritmo = await selectAlgorithm(memoryManager);
        break;
      case "3":
        console.log("Saliendo...");
        process.exit(0);
    }
  }
}
main();
