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

export interface IPositionSummary extends IShiftSummary
{
    role: string;
}

export interface IStaffSummary
{
    daysWorked: number[];
    shiftsWorked: IShiftSummary[];
    sumHoursWorked: number;
    rolesWorked: string[];
}

export class Checker
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
        }, this);

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

        if (!this.checkScheduleEmployees(sub)) return false;
        if (!this.checkScheduleShifts(sub)) return false;

        return true
    }

    private checkScheduleEmployees(sub: S.Submission): boolean
    {
        const employees: T.IStaff[] = this.task.staff;

        employees.forEach((employee) =>
        {
            try {
                const summary = Checker.getEmployeeSummary(employee.name, sub);
            } catch (e) {
                throw new Error("Unable to validate employee '" + employee.name + "': " + e.toString());
            }
        });

        return true;
    }

    private static getEmployeeSummary(name: string, sub: S.Submission): IStaffSummary
    {
        if (libF.isNullOrWhitespace(name)) throw new Error("Invalid employee name.");

        const slotsWorked: IPositionSummary[] = [];

        sub.schedule.days.forEach((day) =>
        {
            day.shifts.forEach((shift) =>
            {
                shift.roster.forEach((position) =>
                {
                    position.people.forEach((positionFilledBy) =>
                    {
                        if (positionFilledBy === name) {
                            slotsWorked.push({
                                role: position.role,
                                start: shift.start,
                                end: shift.end,
                                day: day.day
                            });
                        }
                    });
                });
            });
        });

        const sumHoursWorkedHours: number = slotsWorked.map((slot): number =>
        {
            if (slot.start == null) throw new Error("Invalid start value.");
            if (slot.end == null) throw new Error("Invalid end value.");

            const startHour = slot.start / 100;
            const endHour = slot.end / 100;

            if (startHour < 0 || startHour > 23) throw new Error("Invalid start hour.");
            if (endHour < 0 || endHour > 23) throw new Error("Invalid end hour.");

            return ((endHour + 24) - startHour) % 24;
        }).reduce((accumulated, current): number =>
        {
            return accumulated + current;
        }, 0);

        const sumHoursWorkedMinutes: number = slotsWorked.map((slot): number =>
        {
            const startMin = slot.start % 100;
            const endMin = slot.end % 100;

            if (startMin < 0 || startMin > 59) throw new Error("Invalid start min.");
            if (endMin < 0 || endMin > 59) throw new Error("Invalid end min.");

            return ((endMin + 60) - startMin) % 60;
        }).reduce((accumulated, current): number =>
        {
            return accumulated + current
        }, 0);

        const sumHoursWorked: number = sumHoursWorkedHours + (sumHoursWorkedMinutes / 60);

        var s: IStaffSummary = {
            daysWorked: _.uniq(slotsWorked.map((slot) => { return slot.day }).sort(), true),
            shiftsWorked: slotsWorked.map((slot): IShiftSummary => { return { start: slot.start, end: slot.end, day: slot.day } }),
            sumHoursWorked: sumHoursWorked,
            rolesWorked: _.uniq(slotsWorked.map((slot) => { return slot.role }), false)
        }

        return s;
    }

    private checkScheduleShifts(sub: S.Submission): boolean
    {
        return true;
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
        var filteredRoles: string[] = [];

        if (task.validTask) {
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