export class StateAllocate {
  constructor(
    public state: "ok" | "failed",
    public massage: string,
  ) {}
}