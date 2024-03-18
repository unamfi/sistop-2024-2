import { Process } from "../models/Process";
import { StateAllocate } from "../models/StateAllocate";
import { IAllocationStrategy } from "./IAllocationStrategy";
import { MemoryBlock } from "../models/MemoryBlock";
import { MemorySize } from "models/MemorySize";

export class WorstFitAllocator implements IAllocationStrategy {
  allocate(
    p: Process,
    memorySize: MemorySize,
    memory: MemoryBlock[]
  ): StateAllocate {
    let worstFitIndex = null;
    for (let i = 0; i < memory.length; i++) {
      const block = memory[i];
      if (!block.storedProcess.pid.isNull()) continue;
      if (block.memorySize.value < memorySize.value) continue;
      if (!worstFitIndex) {
        worstFitIndex = i;
        continue;
      }
      const prevBestFit = memory[worstFitIndex];
      if (block.memorySize.value > prevBestFit.memorySize.value) {
        worstFitIndex = i;
      }
    }
    if (worstFitIndex === null) {
      return new StateAllocate(
        "failed",
        "No hay memoria disponible para el proceso"
      );
    }
    let nullBlockToSplit = { ...memory[worstFitIndex] };
    memory[worstFitIndex] = new MemoryBlock(
      p.pid.value,
      memorySize.value,
      memory[worstFitIndex].memoryAddresses.value
    );
    if (nullBlockToSplit.memorySize.value - memorySize.value === 0) {
      return new StateAllocate("ok", "Proceso asignado correctamente");
    }
    nullBlockToSplit.memorySize.value -= memorySize.value;
    nullBlockToSplit.memoryAddresses.value += memorySize.value;
    memory.splice(worstFitIndex + 1, 0, nullBlockToSplit);
    return new StateAllocate("ok", "Proceso asignado correctamente");
  }
}
