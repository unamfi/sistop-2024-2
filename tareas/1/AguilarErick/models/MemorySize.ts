import { GlobalConfigurations } from "../GlobalConfigurations"

export class MemorySize {
    constructor(public value: number) {
        const configurations = GlobalConfigurations.getConfigurations()
        if(value > configurations.MAX_MEMORY_SIZE) {
            throw new Error(`Memory size must be less or equal than ${configurations.MAX_MEMORY_SIZE}`)
        }
        if(value < 1) {
            throw new Error(`Memory size must be greater or equal than 1`)
        }
    }
}