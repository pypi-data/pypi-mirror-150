# stravacookies

`stravacookies` is a small python package providing a few classes for retrieving HTTP cookies from Strava web servers.

These cookies allow web browsers to get the high-resolution version of the Global [Strava Heatmap](https://www.strava.com/heatmap). The very same
cookies can also be used by cartographic applications
(such as [JOSM](https://josm.openstreetmap.de) and
[Cartograph Maps](https://www.cartograph.eu))
to get Strava Heatmap tiles via Tile Map Service
([TMS](https://en.wikipedia.org/wiki/Tile_Map_Service)).

Permission to use the hi-res Strava Heatmap in JOSM has been granted by Strava,
see https://wiki.openstreetmap.org/wiki/Strava
and https://wiki.openstreetmap.org/wiki/Permissions/Strava

## Requirements
The following python packages are also required, and need to be installed:
- `colorama`;
- `mechanize`.

To install them, from the command line run:
```
pip3 install colorama
pip3 install mechanize
```

A Strava account is required. Facebook/Google/Apple login to Strava is not
supported.

## How it works
Hi-res Gloval Strava Heatmap is available to Strava registered users only.
When you click to
https://www.strava.com/heatmap and login to Strava, your browser gets several
cookies that it includes in later requests to be granted permission to download
the hi-res tiles of the Strava Heatmap.

The authentication process consist of three steps:

1. The sser fills the login form at https://strava.com/login.
2. Upon submit, the browser sends a POST request to https://www.strava.com/session,
email=<STRAVA_EMAIL>, password=<STRAVA_PASSWORD>, remember-me checkbox set,
and in exchange it receives `_strava4_session`, `strava_remember_id`, and `strava_remember_token`cookies from the server.
3. The browser sends a GET request to https://heatmap-external-a.strava.com/auth
with the session cookies set, and gets `CloudFront-Signature`, `CloudFront-Policy`, and `CloudFront-Key-Pair-Id` cookies from server.

The last three cookies are those needed to allow the browser to download
the high-res heatmap tiles. Concatenating the cookie strings to the TMS URLs (as
shown below) allows external applications (such as JOSM or Cartograph Maps)
to download the hi-res tiles from Strava.

Example of a TMS URL that can be used in JOSM to get the hi-res version
of the Strava Heatmap:
```
tms[3,15]:https://heatmap-external-{switch:a,b,c}.strava.com/tiles-auth/run/hot/{zoom}/{x}/{y}.png?Key-Pair-Id=<YOUR_KEY_PAIR_ID_COOKIE_VALUE>&Policy=<YOUR_POLICY_COOKIE_VALUE>&Signature=<YOUR_SIGNATURE_COOKIE_VALUE>
```
Cookies expire, so it is necessary to re-login to Strava from time to
time to get up to date cookies.

## Licence
`stravacookies` is distributed under the GPL v3.0 licence.
