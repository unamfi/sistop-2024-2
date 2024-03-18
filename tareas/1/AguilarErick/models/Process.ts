import { ProcessPid } from "../models/ProcessPid";
export class Process {
  public pid: ProcessPid;
  constructor(pid: string) {
    this.pid = new ProcessPid(pid);
  }
}
