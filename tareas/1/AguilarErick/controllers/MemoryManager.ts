import { GlobalConfigurations } from "../GlobalConfigurations";
import { MemoryBlock } from "../models/MemoryBlock";
import { IAllocationStrategy } from "./IAllocationStrategy";
import { FirstFitAllocator } from "./FirstFitAllocator";
import { Process } from "../models/Process";
import { MemorySize } from "../models/MemorySize";
const { MAX_MEMORY_SIZE, PID_OF_NULL_PROCESS } =
  GlobalConfigurations.getConfigurations();
export class MemoryManager {
  private static instance: MemoryManager;
  private lastPid = "A";
  private memoryBlocks: MemoryBlock[];
  private constructor(private allocationStrategy: IAllocationStrategy) {
    this.memoryBlocks = [
      new MemoryBlock(PID_OF_NULL_PROCESS, MAX_MEMORY_SIZE, 0),
    ];
  }
  getMaxFreeContiguousMemorySize() {
    return this.memoryBlocks.reduce((max, block) => {
      if (block.storedProcess.pid.isNull()) {
        return Math.max(max, block.memorySize.value);
      }
      return max
    }, 0)
  }
  deleteProcess({ pid }: Process) {
    const index = this.memoryBlocks.findIndex(
      ({ storedProcess: { pid: storedProcess } }) =>
        storedProcess.value === pid.value
    );
    if (index === -1) {
      throw new Error("The process is not in memory");
    }
    const blockToDeallocate = this.memoryBlocks[index];
    const hasNullMemoryBlockLeft =
      index > 0 &&
      this.memoryBlocks[index - 1].storedProcess.pid.value ===
        PID_OF_NULL_PROCESS;
    const hasNullMemoryBlockRight =
      index < this.memoryBlocks.length - 1 &&
      this.memoryBlocks[index + 1].storedProcess.pid.value ===
        PID_OF_NULL_PROCESS;
    console.log({ hasNullMemoryBlockLeft, hasNullMemoryBlockRight });
    if (hasNullMemoryBlockLeft && hasNullMemoryBlockRight) {
      let leftBlock = this.memoryBlocks[index - 1];
      let rightBlock = this.memoryBlocks[index + 1];
      let {
        memorySize: { value: size },
      } = blockToDeallocate;
      let newMemoryBlock = new MemoryBlock(
        PID_OF_NULL_PROCESS,
        leftBlock.memorySize.value + size + rightBlock.memorySize.value,
        leftBlock.memoryAddresses.value
      );
      this.memoryBlocks[index - 1] = newMemoryBlock;
      this.memoryBlocks.splice(index, 2);
    } else if (hasNullMemoryBlockRight) {
      let rightBlock = this.memoryBlocks[index + 1];
      let {
        memorySize: { value: size },
      } = blockToDeallocate;
      let newMemoryBlock = new MemoryBlock(
        PID_OF_NULL_PROCESS,
        rightBlock.memorySize.value + size,
        blockToDeallocate.memoryAddresses.value
      );
      this.memoryBlocks[index + 1] = newMemoryBlock;
      this.memoryBlocks.splice(index, 1);
    } else if (hasNullMemoryBlockLeft) {
      let leftBlock = this.memoryBlocks[index - 1];
      let {
        memorySize: { value: size },
      } = blockToDeallocate;
      let newMemoryBlock = new MemoryBlock(
        PID_OF_NULL_PROCESS,
        leftBlock.memorySize.value + size,
        leftBlock.memoryAddresses.value
      );
      this.memoryBlocks[index - 1] = newMemoryBlock;
      this.memoryBlocks.splice(index, 1);
    } else if (!hasNullMemoryBlockLeft && !hasNullMemoryBlockRight) {
      this.memoryBlocks[index] = new MemoryBlock(
        PID_OF_NULL_PROCESS,
        blockToDeallocate.memorySize.value,
        blockToDeallocate.memoryAddresses.value
      );
    }
  }
  getMemoryBlocks() {
    return [...this.memoryBlocks];
  }
  insertProcess(p: Process, size: number) {
    return this.allocationStrategy.allocate(
      p,
      new MemorySize(size),
      this.memoryBlocks
    );
  }
  compactMemory() {
    let nullBlockIndex = this.memoryBlocks.findIndex((block) =>
      block.storedProcess.pid.isNull()
    );
    if (nullBlockIndex === -1) return;
    let sizeOfNullBlock = this.memoryBlocks[nullBlockIndex].memorySize.value;
    for (let i = nullBlockIndex + 1; i < this.memoryBlocks.length; i++) {
      const block = this.memoryBlocks[i];
      if (block.storedProcess.pid.isNull()) {
        nullBlockIndex = i;
        sizeOfNullBlock += block.memorySize.value;
        continue;
      }
      this.memoryBlocks[i] = new MemoryBlock(
        block.storedProcess.pid.value,
        block.memorySize.value,
        this.memoryBlocks[nullBlockIndex].memoryAddresses.value
      );
    }
    this.memoryBlocks = this.memoryBlocks.filter(
      (block) => !block.storedProcess.pid.isNull()
    );
    if (this.memoryBlocks.length === 0) {
      const uniqueNullBlock = new MemoryBlock(PID_OF_NULL_PROCESS, 1, 0);
      uniqueNullBlock.memorySize.value = sizeOfNullBlock;
      this.memoryBlocks.push(uniqueNullBlock);
      return;
    }
    const lastBlock = this.memoryBlocks[this.memoryBlocks.length - 1];
    const nullBlock = new MemoryBlock(
      PID_OF_NULL_PROCESS,
      1,
      lastBlock.memoryAddresses.value + lastBlock.memorySize.value
    );
    nullBlock.memorySize.value = sizeOfNullBlock;
    this.memoryBlocks.push(nullBlock);
  }
  public static getInstance(): MemoryManager {
    if (!MemoryManager.instance) {
      MemoryManager.instance = new MemoryManager(new FirstFitAllocator());
    }
    return MemoryManager.instance;
  }
  public changeAllocationStrategy(as: IAllocationStrategy) {
    this.allocationStrategy = as;
  }
  public getPids() {
    return this.memoryBlocks
      .map(({ storedProcess: { pid } }) => {
        return {
          key: pid.value,
          name: "Proceso " + pid.value,
          value: pid.value,
        };
      })
      .filter((block) => block.key !== PID_OF_NULL_PROCESS);
  }
  public getNewPid() {
    const newPid = this.lastPid;
    this.lastPid = String.fromCharCode(newPid.charCodeAt(0) + 1);
    const { VALID_PROCESS_PIDS } = GlobalConfigurations.getConfigurations();
    if (!VALID_PROCESS_PIDS.find((pid) => pid === newPid))
      throw new Error("No more valid pids");
    return newPid;
  }
}
