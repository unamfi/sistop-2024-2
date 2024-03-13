import { GlobalConfigurations } from "../GlobalConfigurations";

export class ProcessPid {
  constructor(public value: string) {
    const configurations = GlobalConfigurations.getConfigurations();
    if (!configurations.VALID_PROCESS_PIDS.includes(value)) {
      throw new Error(`Invalid process pid ${value}`);
    }
  }
  public isNull() {
    return (
      this.value ===
      GlobalConfigurations.getConfigurations().PID_OF_NULL_PROCESS
    );
  }
}
