# Eventbrite CLI

This repository contains a CLI utility to help speed up development with the Eventbrite API

## Setup

`nix-shell`

## Commands

### `redrive`

Use this to resend all failed webhooks between a range of pages for a specific webhook. This
command is useful when an failure if one of your webhook services caused multiple webhooks to
fail and you need to resend all the webhooks after fixing the issue.

This command is able to load the Eventbrite cookies required straight from your browser. Currently,
Brave is supported by default, but the code could easily be changed to support all the browsers that
the `browser-cookie3` module supports.

#### Example

```sh
python -m eb -w 9363299 -e 3 -p "Profile 4"
```

> Redrive all failed webhooks from 9363299 for pages [1, 3] using the cookies from Brave Browser Profile 4.

#### Help

```
Usage: python -m eb [OPTIONS]                                                                       
                                                                                                     
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --webhook-id          -w      TEXT     The webhook ID to redrive [default: None] [required]    │
│ *  --end                 -e      INTEGER  The page number to end on [default: None] [required]    │
│    --profile             -p      TEXT     The name of the Brave Browser profile to use for        │
│                                           cookies                                                 │
│                                           [default: Default]                                      │
│    --start               -s      INTEGER  The page number to start on [default: 1]                │
│    --refresh-cookies     -r               Refresh cookies before starting                         │
│    --install-completion                   Install completion for the current shell.               │
│    --show-completion                      Show completion for the current shell, to copy it or    │
│                                           customize the installation.                             │
│    --help                                 Show this message and exit.                             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
```