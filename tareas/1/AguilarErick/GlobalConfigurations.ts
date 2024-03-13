export class GlobalConfigurations {
    private static instance: GlobalConfigurations
    private readonly configurations = {
        MAX_MEMORY_SIZE: 30,
        MIN_PROCESS_SIZE: 2,
        MAX_PROCESS_SIZE: 15,
        VALID_PROCESS_PIDS : ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J","K", "L", "M", "N", "O", "P", "Q", "R", "S", "T","U", "V", "W", "X", "Y", "Z", "-"],
        PID_OF_NULL_PROCESS: "-"
    }

    private constructor() {
    }

    private static getInstance() : GlobalConfigurations {
        if (!GlobalConfigurations.instance) {
            GlobalConfigurations.instance = new GlobalConfigurations();
        }
        return GlobalConfigurations.instance;
    }

    public static getConfigurations() {
        return GlobalConfigurations.getInstance().configurations;
    }
}