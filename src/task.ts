import * as path from "path";
import * as fs from "fs";

//#region Interfaces

export interface IParameters
{
    maxSuccessiveDays: number;
    doubleShiftsAllowed: boolean;
    useMinMaxHours: boolean;
    useStaffCapabilities: boolean;
}

export interface IStaff
{
    name: string;
    capabilities: string[];
    maxHours: number;
    minHours: number;
}

export interface IPosition
{
    role: string;
    count: number;
}

export interface IShift
{
    start: number;
    end: number;
    positions: IPosition[];
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

export interface ITask
{
    parameters: IParameters;
    staff: IStaff[];
    schedule: ISchedule;
}

//#endregion Interfaces

export class Task implements ITask
{
    constructor(
        filePath: string
    )
    {
        this.load(filePath);
    }

    public load(filePath: string): void
    {
        var fileContents: string;
        this.validTask = false;

        /*
         * First step, read in the file and get its task number
         * Failure here is a problem...
         */
        try {
            fileContents = fs.readFileSync(filePath).toString();
            this.taskNumber = Task.parseTaskNumber(filePath);
        } catch (e) {
            throw new Error("Could not read file or parse task number of input file: " + filePath + ": " + e.toString());
        }

        /*
         * After reading in the file, try to get the JSON object and validate the result.
         * We anticipate having tests with "corrupt" files, so failure here can actually be expected.
         */
        try {
            const taskObj = JSON.parse(fileContents);

            this.parameters = taskObj.parameters;
            this.staff = taskObj.staff;
            this.schedule = taskObj.schedule;

            Task.validate(this);
        } catch (e) {
            console.warn("Input file: " + filePath + " failed loading: " + (<Error>e).message);
            console.warn("WILL CONTINUE");
            return;
        }

        this.validTask = true;
    }

    /**
     * Validates a Task.
     *
     * Throws an error if validation fails.
     * @param task Task to validate.
     */
    public static validate(task: Task): void
    {
        try {
            //TODO: Task validation
            // if ((task.parameters.maxSuccessiveDays || -1) < 0)
            //     throw new Error("maxSuccessiveDays must be 0 or greater");
            // /* The other params (booleans) will later default to FALSE when null: missing values are fine */
        } catch (e) {
            throw new Error("Validation failed: " + (<Error>e).message);
        }
    }

    public static parseTaskNumber(taskPath: string): number
    {
        const match = path.parse(taskPath).name.match(/^input\.(\d+)$/i);
        if (!match)
            throw new Error("Invalid input file name.");

        var taskNum = parseInt(match[1]);
        if (isNaN(taskNum))
            throw new Error("Input number is not a valid integer value");

        return taskNum;
    }

    public parameters: IParameters;
    public staff: IStaff[];
    public schedule: ISchedule;

    public validTask: boolean;
    public taskNumber: number;
}