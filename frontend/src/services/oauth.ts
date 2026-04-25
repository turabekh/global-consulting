import {
  FACEBOOK_APP_ID,
  FACEBOOK_AUTH_URL,
  GOOGLE_AUTH_URL,
  GOOGLE_CLIENT_ID,
  OAUTH_REDIRECT_URI,
  OAUTH_SCOPES,
} from 'src/config/oauth';

type Provider = 'google' | 'facebook';

interface PopupMessage {
  source: 'gc-oauth';
  payload: {
    access_token: string | null;
    error: string | null;
    error_description: string | null;
  };
}

function buildAuthUrl(provider: Provider): string {
  if (provider === 'google') {
    if (!GOOGLE_CLIENT_ID) {
      throw new Error('Google OAuth is not configured');
    }
    const params = new URLSearchParams({
      client_id: GOOGLE_CLIENT_ID,
      redirect_uri: OAUTH_REDIRECT_URI,
      response_type: 'token',
      scope: OAUTH_SCOPES.google,
      include_granted_scopes: 'true',
      prompt: 'select_account',
    });
    return `${GOOGLE_AUTH_URL}?${params.toString()}`;
  }
  if (!FACEBOOK_APP_ID) {
    throw new Error('Facebook OAuth is not configured');
  }
  const params = new URLSearchParams({
    client_id: FACEBOOK_APP_ID,
    redirect_uri: OAUTH_REDIRECT_URI,
    response_type: 'token',
    scope: OAUTH_SCOPES.facebook,
  });
  return `${FACEBOOK_AUTH_URL}?${params.toString()}`;
}

function openCenteredPopup(url: string, title: string): Window | null {
  const width = 500;
  const height = 600;
  const left = window.screenX + (window.outerWidth - width) / 2;
  const top = window.screenY + (window.outerHeight - height) / 2;
  return window.open(url, title, `width=${width},height=${height},left=${left},top=${top}`);
}

export async function getOAuthAccessToken(provider: Provider): Promise<string> {
  const url = buildAuthUrl(provider);
  const popup = openCenteredPopup(url, `${provider}-oauth`);

  if (!popup) {
    throw new Error('Popup was blocked. Please allow popups and try again.');
  }

  return new Promise<string>((resolve, reject) => {
    let settled = false;

    const cleanup = () => {
      window.removeEventListener('message', onMessage);
      window.clearInterval(checkClosed);
    };

    const checkClosed = window.setInterval(() => {
      if (popup.closed && !settled) {
        settled = true;
        cleanup();
        reject(new Error('Sign-in was cancelled'));
      }
    }, 500);

    const onMessage = (event: MessageEvent) => {
      if (event.origin !== window.location.origin) return;
      const data = event.data as PopupMessage | undefined;
      if (!data || data.source !== 'gc-oauth') return;

      settled = true;
      cleanup();
      try {
        popup.close();
      } catch {
        // ignore
      }

      const { access_token, error, error_description } = data.payload;
      if (access_token) {
        resolve(access_token);
      } else {
        reject(new Error(error_description || error || 'OAuth failed'));
      }
    };

    window.addEventListener('message', onMessage);
  });
}
