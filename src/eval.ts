import * as path from "path";
import * as process from "process";
import * as libF from "./lib/functions";
import * as sub from "./submission";
import * as task from "./task";
import * as CheckResult from "./submissionCheckResult";
import * as Checker from "./checker";

export class Evaluator
{
    constructor(
        insOutsPath?: string
    )
    {
        /* Init members */
        if (libF.isNullOrWhitespace(insOutsPath))
            this.sourcesPath = "./test/"
        else
            this.sourcesPath = insOutsPath
        this.tasks = [];
        this.submissions = [];

        /* Try to make the sourcesPath absolute for ease-of-use later */
        try {
            this.sourcesPath = path.resolve(process.cwd(), this.sourcesPath)
        } catch (e) {
            console.error("Error resolving sources path: " + (<Error>e).message);
            console.error("Please fix your arguments and execute again.");
            return;
        }

        /* Load tasks from input files */
        if (!this.loadInputs()) return;
        /* Load submissions from output files */
        if (!this.loadSubmissions()) return;

        this.eval();
    }

    /**
     * Load the Tasks from the Input files
     * @returns Success If false, program execution should stop
     */
    private loadInputs(): boolean
    {
        console.log("Loading inputs...");
        var currentInput: string = "";
        try {
            libF.walk(path.resolve(this.sourcesPath, "inputs/"), false, false).forEach((inputPath) =>
            {
                currentInput = inputPath;
                this.tasks.push(new task.Task(inputPath));
            });
        } catch (e) {
            /*
             * I am anticipating all Errors to be caught during build.
             * If any sneak through to here, I need to figure out what's happening and fix it.
             * Therefore, quit program execution if this catch is fired.
             */
            console.error("Could not load all inputs.");
            console.error("Failed on: " + currentInput);
            console.error("Reason: " + e.toString());
            return false;
        }
        if (debugMode) {
            this.tasks.forEach((task) =>
            {
                console.log("");
                console.log("Task: " + task.taskNumber);
                console.log(JSON.stringify(task));
            });
            console.log("");
        }
        console.log("Loading inputs (" + this.tasks.length + ") DONE.");

        return true;
    }

    /**
     * Load the Submissions for the Output files
     * @returns Success If false, program execution should stop
     */
    private loadSubmissions(): boolean
    {
        console.log("Loading submissions...");
        var currentSubmission: string = "";
        try {
            libF.walk(path.resolve(this.sourcesPath, "outputs/"), false, false).forEach((submissionPath) =>
            {
                currentSubmission = submissionPath;
                this.submissions.push(new sub.Submission(submissionPath));
            });
        } catch (e) {
            /*
             * I am anticipating all Errors to be caught during build.
             * If any sneak through to here, I need to figure out what's happening and fix it.
             * Therefore, quit program execution if this catch is fired.
             */
            console.error("Could not load all submissions.");
            console.error("Failed on: " + currentSubmission);
            console.error("Reason: " + e.toString());
            return false;
        }
        if (debugMode) {
            this.submissions.forEach((submission) =>
            {
                console.log("");
                console.log("Submission: " + libF.join([submission.firstName, submission.lastName, submission.taskNumber], " "));
                console.log(JSON.stringify(submission));
            });
            console.log("");
        }
        console.log("Loading submissions (" + this.submissions.length + ") DONE.")

        return true;
    }

    private eval(): void
    {
        for (let task of this.tasks) {
            var c = new Checker.Checker(task);
            c.checkTaskSubmissions(this.submissions)
        }
    }

    sourcesPath: string;
    tasks: task.Task[];
    submissions: sub.Submission[];
}

process.chdir(__dirname);
export var debugMode: boolean = false;

var inOutPath: string;
if (process.argv.length >= 3)
    inOutPath = process.argv[2];
if (process.argv.length >= 4)
    debugMode = libF.string2Bool(process.argv[3]);

var e = new Evaluator(inOutPath);