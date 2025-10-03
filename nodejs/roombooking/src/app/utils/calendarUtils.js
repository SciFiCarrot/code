import axios from "axios";

export async function getCalendarEntriesCurrentMonth(mail) {
  const calendarEntries = await axios.get('api/calendar?user_mail=' + mail)
  return calendarEntries.data
}
