import { MemoryManager } from "../controllers/MemoryManager";

export class ShowTheCurrentMemory {
  constructor(private memoryManager: MemoryManager) {}
  public show(message = "Asignación actual:") {
    let line = "";
    const memoryBlocks = this.memoryManager.getMemoryBlocks();
    memoryBlocks.forEach(
      ({ storedProcess: { pid }, memorySize: { value }, memoryAddresses }) => {
        for (let i = 0; i < value; i++) {
          line += pid.value;
        }
      }
    );
    console.log(message + "\n");
    console.log(line);
  }
}
