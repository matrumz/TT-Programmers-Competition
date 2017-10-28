import * as R from "./submissionCheckResult";
import * as T from "./task";
import * as S from "./submission";
import * as libF from "./lib/functions";
import * as _ from "underscore";

export interface IShiftSummary
{
    day: number;
    start: number;
    end: number;
}

export interface IStaffSummary
{
    daysWorked: number[];
    shiftsWorked: IShiftSummary[];
    sumHoursWorked: number;
    rolesWorked: string[];
}

class Checker
{
    constructor(
        private task: T.Task
    )
    {
        this.basicTask = Checker.checkForBasicFlag(task);
        this.rolesNeeded = Checker.filterNeededRoles(task);
    }

    private basicTask: boolean;
    private rolesNeeded: string[];

    public checkTaskSubmissions(subs: S.Submission[]): R.SubmissionCheckResult[]
    {
        let results: R.SubmissionCheckResult[] = [];

        subs.forEach((sub) =>
        {
            if (sub.taskNumber != this.task.taskNumber) return;

            results.push(this.check(sub));
        });

        return results;
    }

    private check(sub: S.Submission): R.SubmissionCheckResult
    {
        var result = new R.SubmissionCheckResult(
            sub.firstName,
            sub.lastName,
            null,
            this.task.taskNumber,
            this.basicTask,
            !sub.errored,
            sub.canBeScheduled
        );

        try {
            result.validSchedule = this.checkSchedule(sub);
        } catch (e) {
            throw new Error(
                "Unable to check submission schedule: "
                + libF.join([
                    sub.firstName,
                    sub.lastName,
                    sub.taskNumber
                ])
                + " REASON: "
                + e.toString()
            );
        }

        return result;
    }

    private checkSchedule(sub: S.Submission): boolean
    {
        if (!sub.canBeScheduled) return true;


    }

    private static checkForBasicFlag(task: T.Task): boolean
    {
        return (
            !task.validTask
            || (
                task.parameters.maxSuccessiveDays === 4
                && !task.parameters.doubleShiftsAllowed
                && !task.parameters.useMinMaxHours
                && !task.parameters.useStaffCapabilities
            )
        );
    }

    private static filterNeededRoles(task: T.Task): string[]
    {
        var filteredRoles: string[];

        if (!task.validTask) {
            filteredRoles = []
        }
        else {
            task.schedule.days.forEach((day) =>
            {
                day.shifts.forEach((shift) =>
                {
                    shift.positions.forEach((position) =>
                    {
                        if (position.count > 0)
                            filteredRoles.push(position.role);
                    });
                });
            });
        }

        return _.uniq(filteredRoles);
    }
}