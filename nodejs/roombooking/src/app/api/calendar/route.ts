import { NextRequest, NextResponse } from "next/server";
import settings from "@/app/utils/appSettings";
import { getCalendarEntriesCurrentMonth, initializeGraphForAppOnlyAuth } from "@/app/utils/graphHelper";

export async function GET(req: NextRequest) {
  const url = new URL(req.url);
  const userMail = url.searchParams.get("user_mail");

  if (!userMail) {
    return NextResponse.json(
      { error: 'User email is required' },
      { status: 400 },
    );
  }

  try {
    initializeGraphForAppOnlyAuth(settings);

    const plainCalendarData = await getCalendarEntriesCurrentMonth(userMail);
    const calendarData = plainCalendarData.map((entry: any) => ({
      subject: entry.subject,
      organizer: entry.organizer,
      start: entry.start,
      end: entry.end,
      recurrence: entry.recurrence,
    }));

    return NextResponse.json(calendarData);
  } catch (error) {
    return NextResponse.json(
      { message: 'Failed to fetch calendar entries: ' + error },
      { status: 500 },
    );
  }
}
