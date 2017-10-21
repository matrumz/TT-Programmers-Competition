import * as path from "path";
import * as process from "process";
import * as libF from "./lib/functions";
import * as sub from "./submission";
import * as task from "./task";


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

        try {
            this.sourcesPath = path.resolve(process.cwd(), this.sourcesPath)
        } catch (e) {
            console.error("Error resolving sources path: " + (<Error>e).message);
            console.error("Please fix your arguments and execute again.");
            return;
        }

        console.log("Loading inputs...");
        var currentInput: string = "";
        try {
            libF.walk(path.resolve(this.sourcesPath, "inputs/"), false, false).forEach((inputPath) =>
            {
                currentInput = inputPath;
                this.tasks.push(new task.Task(inputPath));
            });
        } catch (e) {
            console.error("Could not load all inputs.");
            console.error("Failed on: " + currentInput);
            console.error("Reason: " + (<Error>e).message);
            return;
        }
        console.log("Loading inputs DONE.");
        if (debugMode)
            this.tasks.forEach((task) =>
            {
                console.log(JSON.stringify(task));
            });
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