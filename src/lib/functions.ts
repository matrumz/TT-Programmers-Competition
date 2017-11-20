import * as fs from "fs";
import * as path from "path";

/**
 * Returns true if the passed string is NULL, empty, or just whitespace.
 * @param str The string to test
 */
export function isNullOrWhitespace(str: string): boolean
{
    return str === null || (str || "").match(/^\s*$/) !== null;
}

/**
 * Generate a list of all files under the specified directory. Recursive search optional.
 * @param dir The dir to begin searching from
 * @param recursive TRUE if file list should include files in sub-directories
 */
export function walk(dir: string, recursive: boolean, relativeResults: boolean = false): string[]
{
    /* Ignore null directory input */
    if (isNullOrWhitespace(dir))
        return [];

    /* Initialize list */
    var filesList: string[] = [];

    /* Get a list of directory contents & ensure an empty array if null returned */
    var directoryContents = fs.readdirSync(dir) || [];

    directoryContents.forEach((item) =>
    {
        /* Get the absolute path and stats of the item */
        var fullItem = relativeResults ? (path.relative(process.cwd(), dir) + path.sep + item) : path.resolve(dir, item);
        var itemStat = fs.statSync(fullItem);
        /* Handle item based on type */
        if (itemStat.isFile())
            filesList.push(fullItem);
        else if (itemStat.isDirectory() && recursive)
            /* Will recursively call when directory found and if requested */
            filesList = filesList.concat(walk(fullItem, recursive, relativeResults));
        /* not handling sym-links at the mo' */
    });

    return filesList;
}

export function string2Bool(str: string): boolean
{
    str = (str || "false").toLowerCase();

    switch (str) {
        case 'y':
        case 'yea':
        case 'yes':
        case 'true':
        case '1':
            return true;
        default:
            return false;
    }
}

/**
 * Takes an array and returns the string representation of the items separated by an optional delimiter.
 * @param a Array of anything with toString() defined
 * @param delim An optional delimiter, that will be placed between each element of the array. DEFAULT: ","
 */
export function join(a: any[], delim: string = ","): string
{
    var result: string = "";
    a.forEach((e, index) =>
    {
        result += (e || "").toString();
        if (index < (a.length - 1))
            result += delim;
    });

    return result;
}

/**
 * Checks if the first value is between the next two values (low/high), optionally exclusively.
 * @param check Number to check
 * @param l Lower bound
 * @param h Upper bound
 * @param inclusive Should the check be inclusive of the bounds?
 */
export function between(check: number, l: number, h: number, inclusive: boolean = true): boolean
{
    if (check == null || l == null || h == null) return false;

    if (inclusive)
        return l <= check && check <= h;
    else
        return l < check && check < h;
}