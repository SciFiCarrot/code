"use client"

import { useQuery, QueryClientProvider, QueryClient } from "@tanstack/react-query";
import { getCalendarEntriesCurrentMonth } from "@/app/utils/calendarUtils";
import { getEventInfo } from "@/app/utils/eventInfo";
import { formatDateTime } from "@/app/utils/dateUtils";
import moment from "moment-timezone";
import RootLayout from "./layout";
import RoomStatusContainer from "@/components/RoomStatusContainer";
import { useEffect, useState } from "react";

const queryClient = new QueryClient();

export default function Home() {
  return (
    <QueryClientProvider client={queryClient}>
      <HomeContent />
    </QueryClientProvider>
  );
}


function HomeContent() {
  // Add state to track current time
  const [now, setNow] = useState(moment().tz(moment.tz.guess()));

  // Update time every minute
  useEffect(() => {
    const interval = setInterval(() => {
      setNow(moment().tz(moment.tz.guess()));
    }, 60000); // 60 seconds

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);
  

  const calendarName = "luis.conradty"
  // Add refetchInterval to query
  const { data, error, isLoading } = useQuery({
    queryKey: ["calendar"],
    queryFn: () => getCalendarEntriesCurrentMonth(calendarName+"@digiclub-germering.de"),
    refetchInterval: 60000, // Refetch every minute
  });
  if (isLoading) return <div className="text-center mt-4">Loading...</div>;
  if (error) return <div className="text-center mt-4 text-red-500">Error: {error.message}</div>;


  const currentEvent = data.find((event: any) => {
    const start = moment.utc(event.start.dateTime).tz(moment.tz.guess());
    const end = moment.utc(event.end.dateTime).tz(moment.tz.guess());
    return start <= now && end >= now;
  });

  const nextEvent = data.find((event: any) => moment.utc(event.start.dateTime).tz(moment.tz.guess()) > now);
  const isFreeToday = !data.some((event: any) => {
    const start = moment.utc(event.start.dateTime).tz(moment.tz.guess());
    return start.isSame(now, 'day') && start > now;
  });

  const roomStatus = currentEvent ? "busy" :
    (nextEvent && moment.utc(nextEvent.start.dateTime).tz(moment.tz.guess()).diff(now, 'minutes') <= 30) ?
      "soon" : "free";

  const nextMeetingName = nextEvent.subject 


  let status = "free";
  if (currentEvent) {
    status = "busy";
  } else if (nextEvent && moment(nextEvent.start.dateTime).tz(moment.tz.guess()).diff(now, 'minutes') <= 30) {
    status = "soon";
  }

  let CheckIn = False
  function handleCheckIn() {
    const CheckIn = True
  } 

/*
function getEventInfo(event: Event, now: moment.Moment) {
  const start = moment.utc(event.start.dateTime).tz(moment.tz.guess());
  const end = moment.utc(event.end.dateTime).tz(moment.tz.guess());
  const nowMs = now.valueOf();
  const startMs = start.valueOf();
  const endMs = end.valueOf();
  const durationMs = endMs - startMs;
  const timeLeftMin = ((endMs - nowMs) / 60000) | 0;
  const name = Event.subject
  const organizer = Event.organizer.emailAddress.name
  

  return {
    progressBarValue: (nowMs - startMs) / durationMs,
    durationH: (durationMs / 3600000) | 0,
    durationM: ((durationMs / 60000) | 0) % 60,
    timeLeftH: (timeLeftMin / 60) | 0,
    timeLeftM: timeLeftMin % 60,
  };
}
*/
  // Nutzung:
  const currentInfo = currentEvent ? getEventInfo(currentEvent, now) : null;
  const nextInfo = nextEvent ? getEventInfo(nextEvent, now) : null;

/*
  let progressBarValue = 0;
  let timeLeft = 0;
  let duration = 0;
  let durationH = 0;
  let durationM = 0;
  let timeLeftM = 0;
  let timeLeftH = 0;
  if (currentEvent) {
    const start = moment.utc(currentEvent.start.dateTime).tz(moment.tz.guess());
    const end   = moment.utc(currentEvent.end.dateTime).tz(moment.tz.guess());
    progressBarValue = (now.valueOf() - start.valueOf()) /
                       (end.valueOf() - start.valueOf());
    timeLeft = ((end.valueOf() - now.valueOf())/60000) | 0 
    duration = end.valueOf()-start.valueOf()

    durationH = duration /(60000*60) | 0
    durationM = (duration / 60000 | 0) % 60
  }  
  function convertTime(duration) {
    hours = duration /(60000*60) | 0
    minutes = (duration / 60000 | 0) % 60
  }
  timeLeftH = timeLeft /(60) | 0
  timeLeftM = (timeLeft  | 0) % 60
*/

 // const progressBarValue = (now - start) / (end - start)
  // value = (now - start) / (end - start)


  const roomName = calendarName 


  return (
    <RoomStatusContainer status={roomStatus}> 
      
      <div className="flex items-center justify-center h-full text-center p-4">
        {currentEvent ? (
          <div>
            <div>
              <h2 className="text-8xl p-10">{currentInfo.timeLeftH > 0 ? `${currentInfo.timeLeftH}h ` : ""}{currentInfo.timeLeftM}min übrig</h2>
              <h2 className="text-4xl">{currentInfo.name} ({currentInfo.organizer})</h2>
            </div>
            <progress value={currentInfo.progressBarValue} max="1" className="w-64 h-3 accent-purple-600">
            </progress>
            <button className="m-9 p-2 w-30 bg-blue-600 text-white rounded onClick={handleCheckIn}">Check-In</button>
            <h4>{currentInfo.durationH}h {currentInfo.durationM}min</h4>
          </div>          

        ) : (

          <div>
            {isFreeToday ? (
              <div>
                <h1 className="text-8xl p-10">
                  {roomName}
                </h1>
                <h3 className="text-4xl">VERFÜGBAR</h3>
                <div>
                  <h2 className="text-2xl">Spontanmeeting buchen</h2>
                  <div>
                    <button className="m-9 p-2 w-30 bg-blue-600 text-white rounded">15 min</button>
                    <button className="m-9 p-2 w-30 bg-blue-600 text-white rounded">30 min</button>
                    <button className="m-9 p-2 w-30 bg-blue-600 text-white rounded">1 h</button>
                  </div>
                </div>
              </div>
               
            ) : (

              <div>

                <h2>Frei bis {nextMeeting}</h2>
              </div>
            )}
          </div>
        )}
      </div>
    </RoomStatusContainer>
  );
}
