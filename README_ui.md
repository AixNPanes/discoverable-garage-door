# Lovelace example for discoverable-garage-door

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Requirements](#requirements)
  - [Raspberry PI](#raspberry-pi)
  - [Debian](#debian)
  - [Python](#python)
- [Installing](#installing)
  - [installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
  - [Format](#format)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Prerequisites

### Install the module if you haven't already

python3.11 pip install discoverable-garage-door

### Run the module

python3.11 -m discoverable-garage-door

### Create a button helper

- Edit your Home Asistant configuration.yaml file one of the following methods (or another of your choice):
    - Addon - File Helper
    - Addon - Visual Studio Code
    - If you're using docker to run home assistant:
      - sudo docker exec -it `sudo docker ps|grep 'homeassistant:'|cut -d' ' -f1  -` bash
      - vi
- open the configuration.yaml file in the /config folder
- add the following to the configuration.yaml in the /config folder:

        input_button:
          garage_door_opener:
            name: My Garage Door

- If there is no input_button: in the existing system configuration.yaml, just add the new data to the bottom
- If there is an existing input_button: add the configuration.yaml from the examples folder to the system's configuration.yaml after the last part of the existing input_select: statement, but delete the input_select: statement from the data you just added. There should only be a single input_select: statement in the resulting system configuration.yaml
- Enable your changes by clicking Developer Tools->YAML->Check Configuration. If you get Configuration will not prevent Home Assistant from starting! everything's OK. If you get an error or it seems to take a long time, fix it before you continue. Notifications or logs (use the editor like above) may help.
- Click RESTART, then Quick Restart
- Click Settings->Helpers. Your Input Button should appear as a helper.
- Click Settings->Entities. Your Input Button should appear as an entity.

### Create your Button

- Click Overview
- Click the three vertical dots in the top right of the Home Assistant pane (not the 3 vertical dots in the top right of the browser window)
- Click Edit Dashboard
- Click Raw configuration Editor
- Add the following to the end of the file

      - title: Doors
        path: Doors
        badges: []
        cards:
          - square: false
            type: grid
            title: Doors
            view_layout:
              grid-area: Doors
            columns: 3
            cards:
              - type: custom:button-card
                entity: cover.my_garage_door
                name: Garage Door
                layout: vertical
                show_state: true
                show_name: true
                state:
                  - value: open
                    color: yellow
                    card:
                      - filter: opacity(50%)
                  - value: opening
                    color: red
                    card:
                      - filter: opacity(50%)
                  - value: closed
                    color: green
                    card:
                      - filter: opacity(50%)
                  - value: closing
                    color: red
                    card:
                      - filter: opacity(50%)
                tap_action:
                  action: call-service
                  service: cover.close_cover
                  service_data:
                    entity_id: cover.my_garage_door
  
- Click Save
- Close the editor by clickgin the X to the left of the Editor title
- This will create a new Doors view on the right hand end of Home
- Click Done in the upper right. The garage door should be shown.

