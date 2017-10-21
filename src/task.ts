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
        path: string
    )
    {
        this.load(path);
    }

    public load(path: string): void
    {
        try {
            var taskObj: ITask = JSON.parse(fs.readFileSync(path).toString())

            this.parameters = taskObj.parameters;
            this.staff = taskObj.staff;
            this.schedule = taskObj.schedule;

            Task.validate(this);
        } catch (e) {
            throw new Error("Could not load input file: " + path + ": " + (<Error>e).message);
        }
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

    parameters: IParameters;
    staff: IStaff[];
    schedule: ISchedule;
}