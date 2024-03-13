import { Process } from "../models/Process";
import { StateAllocate } from "../models/StateAllocate";
import { IAllocationStrategy } from "./IAllocationStrategy";
import { MemoryBlock } from "../models/MemoryBlock";
import { MemorySize } from "models/MemorySize";

export class FirstFitAllocator implements IAllocationStrategy {
  allocate(
    p: Process,
    sizeOfProcess: MemorySize,
    memory: MemoryBlock[]
  ): StateAllocate {
    for (let i = 0; i < memory.length; i++) {
      const { memorySize, storedProcess, memoryAddresses } = memory[i];
      if (!storedProcess.pid.isNull()) continue;
      if (memorySize.value < sizeOfProcess.value) continue;
      const newBlock = new MemoryBlock(
        p.pid.value,
        sizeOfProcess.value,
        memoryAddresses.value
      );
      memory[i] = newBlock;
      if ((memorySize.value - sizeOfProcess.value) === 0) {
        return new StateAllocate("ok", "Proceso asignado correctamente");
      }
      const nullBlock = new MemoryBlock(
        storedProcess.pid.value,
        (memorySize.value -= sizeOfProcess.value),
        (memoryAddresses.value += sizeOfProcess.value)
      );
      memory.splice(i + 1, 0, nullBlock);
      return new StateAllocate("ok", "Proceso asignado correctamente");
    }
    return new StateAllocate("failed", "No se pudo asignar el proceso");
  }
}
