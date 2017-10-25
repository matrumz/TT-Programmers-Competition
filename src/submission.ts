import * as path from "path";
import * as fs from "fs";

//#region Interfaces

export interface IPosition
{
    role: string;
    people: string[];
}

export interface IShift
{
    start: number;
    end: number;
    roster: IPosition[];
}

export interface IDay
{
    day: number;
    shifts: IShift[];
}

export interface ISchedule
{
    roles: string[];
    days: IDay[];
}

export interface ISubmission
{
    canBeScheduled: boolean;
    schedule: ISchedule;
}

//#endregion

export class Submission implements ISubmission
{
    constructor(
        filePath: string
    )
    {
        this.errored = false;
        this.load(filePath)
    }

    public load(filePath: string): void
    {
        var fileContents: string;

        /* No failures will be tolerated... you have been warned mwaahahahahaha */
        try {
            fileContents = fs.readFileSync(filePath).toString();
            this.parseFileName(filePath);
        } catch (e) {
            this.error("Could not load submission file: " + filePath + ": " + e.toString());
            return;
        }

        try {
            const submissionObj = JSON.parse(fileContents);

            this.canBeScheduled = submissionObj.canBeScheduled;
            this.schedule = submissionObj.schedule;

            /* What's here is here. There will be no validation. It either passes the evaluation later, or it fails */
        } catch (e) {
            this.error("Failed to load submission object for file: " + filePath + ": " + e.toString());
            return;
        }
    }

    public parseFileName(filePath: string): void
    {
        const match = path.parse(filePath).name.match(/(^\w+)\.(\w+)\.(\d+)$/i);
        if (!match) {
            this.error("Invalid submission file name.");
            return;
        }

        this.firstName = match[1];
        this.lastName = match[2];
        this.taskNumber = parseInt(match[3]);
        if (isNaN(this.taskNumber)) {
            this.error("Input number is not a valid integer value.");
        }
    }

    private error(msg: string): void
    {
        this.errored = true;
        this.errorReason = msg || "UNKNOWN";
    }

    public canBeScheduled: boolean;
    public schedule: ISchedule;

    public firstName: string;
    public lastName: string;
    public taskNumber: number;

    public errored: boolean;
    public errorReason: string;
}