export const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || '';
export const FACEBOOK_APP_ID = import.meta.env.VITE_FACEBOOK_APP_ID || '';

export const GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth';
export const FACEBOOK_AUTH_URL = 'https://www.facebook.com/v18.0/dialog/oauth';

export const OAUTH_REDIRECT_URI = `${window.location.origin}/oauth-callback.html`;
export const OAUTH_SCOPES = {
  google: 'openid email profile',
  facebook: 'email,public_profile',
};
