import { GlobalConfigurations } from "../GlobalConfigurations"

export class MemoryAddress {
    constructor(public value: number) {
        const configurations = GlobalConfigurations.getConfigurations()
        if(value < 0) {
            throw new Error(`Memory address must be greater or equal than 0`)
        }
        if(value > configurations.MAX_MEMORY_SIZE) {
            throw new Error(`Memory address must be less or equal than ${configurations.MAX_MEMORY_SIZE}`)
        }
    }
}