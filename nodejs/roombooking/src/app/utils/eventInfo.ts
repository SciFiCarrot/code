import moment from "moment-timezone";
export function getEventInfo(event: Event, now: moment.Moment) {
  const start = moment.utc(event.start.dateTime).tz(moment.tz.guess());
  const end = moment.utc(event.end.dateTime).tz(moment.tz.guess());
  const nowMs = now.valueOf();
  const startMs = start.valueOf();
  const endMs = end.valueOf();
  const durationMs = endMs - startMs;
  const timeLeftMin = ((endMs - nowMs) / 60000) | 0;
  const name = event.subject
  const organizer = event.organizer.emailAddress.name
  

  return {
    progressBarValue: (nowMs - startMs) / durationMs,
    durationH: (durationMs / 3600000) | 0,
    durationM: ((durationMs / 60000) | 0) % 60,
    timeLeftH: (timeLeftMin / 60) | 0,
    timeLeftM: timeLeftMin % 60,
    name: name,
    organizer: organizer,
  };
}
