// Django Time String example: "2023-11-02T17:23:00.318484Z"

export function parseDjangoTimeString(timeString: string): number {
    let millisecondsPart = timeString.slice(23, -1);
    let truncatedMilliseconds = millisecondsPart.slice(0, -3);
    let isoTimeString = timeString.replace(
        millisecondsPart,
        truncatedMilliseconds,
    );

    return Date.parse(isoTimeString);
}

export function toDjangoTimeString(dateObject: Date): string {
    const ISOString = dateObject.toISOString();
    return ISOString.slice(0, 23) + ISOString.slice(26, 27);
}

function getUserTimezone() {
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
}

export function formatTimeShort(djangoTimeString: string): string {
    try {
        const formatterThisYear = new Intl.DateTimeFormat("en-US", {
            month: "long",
            day: "numeric",
            year: "numeric",
            timeZone: getUserTimezone(),
        });

        const formatterPastYearOrOlder = new Intl.DateTimeFormat("en-US", {
            month: "long",
            day: "numeric",
            timeZone: getUserTimezone(),
        });

        const parsedTimeNumber = parseDjangoTimeString(djangoTimeString);

        const parsedYear = new Date(parsedTimeNumber).getFullYear();
        const currentYear = new Date().getFullYear();

        // console.log(formatterThisYear.format(parsedTimeNumber))

        if (currentYear === parsedYear) {
            return formatterPastYearOrOlder.format(parsedTimeNumber);
        } else {
            return formatterThisYear.format(parsedTimeNumber);
        }
    } catch (error) {
        console.log(`Error trying to format time: ${error}`)
        return ""
    }

}
