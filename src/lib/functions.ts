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