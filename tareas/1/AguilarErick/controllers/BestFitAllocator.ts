import { Process } from "../models/Process";
import { StateAllocate } from "../models/StateAllocate";
import { IAllocationStrategy } from "./IAllocationStrategy";
import { MemoryBlock } from "../models/MemoryBlock";
import { MemorySize } from "models/MemorySize";

export class BestFitAllocator implements IAllocationStrategy {
  allocate(
    p: Process,
    memorySize: MemorySize,
    memory: MemoryBlock[]
  ): StateAllocate {
    let bestFitIndex = null;
    for (let i = 0; i < memory.length; i++) {
      const block = memory[i];
      if (!block.storedProcess.pid.isNull()) continue;
      if (block.memorySize.value < memorySize.value) continue;
      if (!bestFitIndex) {
        bestFitIndex = i
        continue;
      }
      const prevBestFit = memory[bestFitIndex];
      if (block.memorySize.value < prevBestFit.memorySize.value) {
        bestFitIndex = i;
      }
    }
    if (bestFitIndex === null) {
      return new StateAllocate(
        "failed",
        "No hay memoria disponible para el proceso"
      );
    }
    let nullBlockToSplit = {...memory[bestFitIndex]}
    memory[bestFitIndex] = new MemoryBlock(
      p.pid.value,
      memorySize.value,
      memory[bestFitIndex].memoryAddresses.value
    )
    if((nullBlockToSplit.memorySize.value - memorySize.value) === 0) {
      return new StateAllocate("ok", "Proceso asignado correctamente");
    }
    nullBlockToSplit.memorySize.value -= memorySize.value
    nullBlockToSplit.memoryAddresses.value += memorySize.value
    memory.splice(bestFitIndex + 1, 0, nullBlockToSplit)
    return new StateAllocate("ok", "Proceso asignado correctamente");
  }
}
