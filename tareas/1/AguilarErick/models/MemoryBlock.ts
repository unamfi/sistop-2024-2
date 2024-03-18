import { MemoryAddress } from "./MemoryAddress"
import { MemorySize } from "./MemorySize"
import { Process } from "./Process"
export class MemoryBlock {
    public storedProcess : Process
    public memoryAddresses : MemoryAddress
    public memorySize : MemorySize
    constructor(storedProcessPid: string, size: number, startAddress: number) {
        this.storedProcess = new Process(storedProcessPid)
        this.memoryAddresses = new MemoryAddress(startAddress)
        this.memorySize = new MemorySize(size)
    }
}