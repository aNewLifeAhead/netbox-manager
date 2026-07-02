# CJ's NetBox Sync

A personal NetBox plugin developed by Charles Wright to keep device components synchronised with their Device Type templates.

This branch contains the version currently running on my business NetBox instance and includes my own branding, UI improvements and experimental features before they are merged into the public release.

---

## Purpose

I started a new NetBox instance within my business, there was lots to learn but I found I was having to delete device instances as I was adding interfaces/power ports etc to device types.

I couldn't find a way to sync them so wrote this plugin so I can update device instances post deployment.

From my early understanding of how NetBox works, NetBox only applies Device Type templates when a device is first created, leaving existing devices out of sync.

This plugin solves that problem by safely comparing every device against its Device Type and creating any missing components.

Existing components are **never modified or removed**, making it safe to run multiple times.

---

## Features

- ✔ Synchronise Device Type components
- ✔ Dry Run mode
- ✔ Commit mode
- ✔ Safe and repeatable
- ✔ Integrated into the NetBox **Tools** menu
- ✔ Detailed output showing exactly what will change

Currently supports:

- Interfaces
- Console Ports
- Console Server Ports
- Power Ports
- Power Outlets
- Rear Ports
- Front Ports
- Module Bays
- Device Bays

---

## Why this branch exists

This branch contains my personal production customisations, including:

- CJ branding
- UI tweaks
- Additional descriptions
- Experimental features
- Work in progress before merging into `main`

The `main` branch remains the clean, generic version intended for public use.

---

## Current Status

🟢 Running on my production NetBox instance.

This branch is actively developed alongside my home lab and production network.

---

## Planned Features

- Progress indicator
- Background job execution
- Filter by Device Type
- Filter by Device
- Scheduled synchronisation
- Better reporting
- Sync history
- Component summary statistics
- Logging improvements

---

## Repository Structure

```
main
    Public release

cj-customisation
    My production branch with custom branding and in-development features
```

---

## Author

**Charles Wright**

Built for my own NetBox environment and shared in the hope it may be useful to others.

---

*"If I have to do something more than once, I'm probably going to automate it."*
