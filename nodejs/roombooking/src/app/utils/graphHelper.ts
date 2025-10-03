// graphHelper.ts
import 'isomorphic-fetch';
import { ClientSecretCredential } from '@azure/identity';
import { Client } from '@microsoft/microsoft-graph-client';
import { TokenCredentialAuthenticationProvider } from '@microsoft/microsoft-graph-client/authProviders/azureTokenCredentials/index.js';

interface Settings {
  clientId: string;
  clientSecret: string;
  tenantId: string;
}

interface CalendarEntry {
  subject: string;
  organizer: { emailAddress: { name: string; address: string } };
  start: { dateTime: string };
  end: { dateTime: string };
  recurrence?: { pattern: { type: string } };
}

let _settings: Settings | undefined = undefined;
let _clientSecretCredential: ClientSecretCredential | undefined = undefined;
let _appClient: Client | undefined = undefined;

export function initializeGraphForAppOnlyAuth(settings: Settings): void {
  if (!settings) {
    throw new Error('Settings cannot be undefined');
  }

  _settings = settings;

  if (!_clientSecretCredential) {
    _clientSecretCredential = new ClientSecretCredential(
      _settings.tenantId,
      _settings.clientId,
      _settings.clientSecret,
    );
  }

  if (!_appClient) {
    const authProvider = new TokenCredentialAuthenticationProvider(
      _clientSecretCredential,
      {
        scopes: ['https://graph.microsoft.com/.default'],
      },
    );

    _appClient = Client.initWithMiddleware({
      authProvider: authProvider,
    });
  }
}

export async function getCalendarEntriesCurrentMonth(email: string): Promise<CalendarEntry[]> {
  if (!_appClient) {
    throw new Error('Graph has not been initialized for app-only auth');
  }

  const now = new Date();
  const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1).toISOString();
  const endOfMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0).toISOString();

  let events: CalendarEntry[] = [];
  let response = await _appClient
    ?.api(`/users/${email}/calendarView`)
    .query({
      startDateTime: startOfMonth,
      endDateTime: endOfMonth,
      $top: 50,
    })
    .select(['subject', 'organizer', 'start', 'end', 'recurrence'])
    .orderby('start/dateTime')
    .get();

  events = events.concat(response.value);

  while (response['@odata.nextLink']) {
    response = await _appClient.api(response['@odata.nextLink']).get();
    events = events.concat(response.value);
  }

  return events;
}
