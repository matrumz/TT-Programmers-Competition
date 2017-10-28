import { ISubmitter } from "./models/ISubmitter";
import { join } from "./lib/functions";

export class SubmissionCheckResult
{
    constructor(
        public firstName?: string,
        public lastName?: string,
        public code?: string,
        public taskNumber?: number,
        public basicTask?: boolean,
        public outputLoaded?: boolean,
        public canBeScheduled?: boolean,
        public validSchedule?: boolean
    ) { }

    public toString(): string
    {
        return join([
            (this.firstName || ""),
            (this.lastName || ""),
            (this.code || ""),
            (this.taskNumber || ""),
            this.excelifyBoolean(this.basicTask),
            this.excelifyBoolean(this.outputLoaded),
            this.excelifyBoolean(this.canBeScheduled),
            this.excelifyBoolean(this.validSchedule)
        ], ",");
    }

    private excelifyBoolean(b: boolean): '1'|'0'
    {
        return (b ? '1' : '0');
    }
}