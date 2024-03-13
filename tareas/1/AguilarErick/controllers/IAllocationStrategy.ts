import { MemorySize } from "models/MemorySize";
import { MemoryBlock } from "../models/MemoryBlock";
import { Process } from "../models/Process";
import { StateAllocate } from "../models/StateAllocate";

export interface IAllocationStrategy {
    allocate(p:Process, memorySize: MemorySize, memory : MemoryBlock[]) : StateAllocate
}