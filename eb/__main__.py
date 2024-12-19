import re
from eb.CachedCookieJar import CachedCookieJar
from eb.BrowserSession import BrowserSession

from bs4 import BeautifulSoup
import os
import typer

BASE_URL = 'https://www.eventbrite.com'
WEBHOOK_URL = f'{BASE_URL}/account-settings/webhooks'
WEBHOOK_RESEND_URL = f'{WEBHOOK_URL}/resend/'
COOKIE_CACHE_FILE = '.cookies.pkl'

app = typer.Typer()

@app.command()
def redrive(
    webhook_id: str = typer.Option(..., '--webhook-id', '-w', help='The webhook ID to redrive',),
    end: int = typer.Option(..., '--end', '-e', help='The page number to end on'),
    profile: str = typer.Option('Default', '--profile', '-p', help='The name of the Brave Browser profile to use for cookies'),
    start: int = typer.Option(1, '--start', '-s', help='The page number to start on'),
    refresh_cookies: bool = typer.Option(False, '--refresh-cookies', '-r', help='Refresh cookies before starting'),
):
    if start > end:
        print('Start page must be less than or equal to end page')
        return
    
    if start < 1:
        print('Start page must be greater than 0')
        return
    
    cookie_file = f'{os.environ["HOME"]}/Library/Application Support/BraveSoftware/Brave-Browser/{profile}/Cookies'

    if not os.path.exists(cookie_file):
        print('Cookies file not found: ', cookie_file)
        return
    
    if refresh_cookies:
        os.remove(COOKIE_CACHE_FILE)
    
    with BrowserSession(
        CachedCookieJar(
            '.eventbrite.com', 
            cookie_file, 
            COOKIE_CACHE_FILE
        ),
        {
            'Origin': 'https://www.eventbrite.com',
            'Referer': 'https://www.eventbrite.com/',
        }
    ) as session:
        failure_count = 0

        for page in range(start, end + 1):
            print(f'Processing page {page}...')
            r = session.get(f'{WEBHOOK_URL}/{webhook_id}?page={page}')

            soup = BeautifulSoup(r.text, 'html5lib')
            webhook_form = soup.find('form', {'id': 'resend-form'})
            csrfmiddlewaretoken = webhook_form.find('input', {'name': 'csrfmiddlewaretoken'})['value']
            error_row_badges = soup.find_all('span', {'class': 'badge--error'})

            for badge in error_row_badges:
                event_id = re.search(r'Request ID: (\d+)', badge.parent.text).group(1)

                payload = {
                    'csrfmiddlewaretoken': csrfmiddlewaretoken,
                    'webhook_id': webhook_id,
                    'delivery_request_id': event_id,
                }
                
                r = session.post(WEBHOOK_RESEND_URL, data=payload, allow_redirects=False)

                if r.ok:
                    print(f'Resent: status={r.status_code}, webhook_event_id={event_id}')
                    failure_count = 0
                else:
                    print(f'Failed to resend: status={r.status_code}, webhook_event_id={event_id}')
                    failure_count += 1
                    if failure_count > 5:
                        print('Too many failures, exiting...')
                        return
                    # TODO: handle failed requests, detect if logged out or rate limited and grab fresh cookies
                    # with (open('failed.html', 'w')) as f:
                    #     f.write(r.text)

if __name__ == '__main__':
    app()