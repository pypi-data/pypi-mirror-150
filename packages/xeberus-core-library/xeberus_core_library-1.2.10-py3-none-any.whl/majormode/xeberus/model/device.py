# Copyright (C) 2019 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

import uuid

from majormode.perseus.model.geolocation import GeoPoint
from majormode.perseus.utils import cast
from majormode.perseus.utils.date_util import ISO8601DateTime

from majormode.xeberus.constant.device import BatteryStateEventType


class Event:
    def __eq__(self, other):
        return self._event_ref == other.event_ref

    def __init__(
            self,
            event_ref,
            event_time):
        self._event_ref = event_ref
        self._event_time = event_time

    @property
    def event_ref(self):
        return self._event_ref

    @property
    def event_time(self):
        return self._event_time


class BatteryStateChangeEvent(Event):
    """
    Event that notifies from the change of the state of the internal
    battery of a mobile device, such as:

    - the device is connected to or disconnected from the power source of
      the vehicle this device is mounted on;

    - the level of the device's battery increases or decreases.

    Only devices equipped with an internal battery can post this
    notification.  A device not equipped with an internal battery is
    indeed less secure as it is not able to send any notification when it
    is disconnected from the power source of the vehicle this device is
    mounted on; the device is immediately switched off.
    """
    def __init__(
            self,
            event_ref: str,
            event_type: BatteryStateEventType,
            event_time: ISO8601DateTime,
            battery_level: float,
            location: GeoPoint = None):
        """
        Build a new object `BatteryStateChangeEvent`.


        @param event_ref: The reference of this event as given by the client
             application running on the mobile device that reported this event.

             This information is used to detect events that the mobile device would
             report multiple times.  This happens when network outage occurs after
             the client application reported successfully a batch of events, but
             the network connection with the cloud service timed out before the
             client application had the chance to receive the acknowledgement from
             the cloud service.  Therefore, the client application reattempts to
             report one more time these events.

        @param event_type: An item of the enumeration `BatteryStateEventType`
            that indicates the type of event that occurred.

        @param event_time: The time when this event occurred.

        @param battery_level: The level in percentage of the device's internal
            battery when this even occurred.

        @param location: The last known
            location of the device when this event occurred.
        """
        super().__init__(event_ref, event_time)
        self._event_type = event_type
        self._battery_level = battery_level
        self._location = location

    @property
    def battery_level(self):
        return self._battery_level

    @property
    def event_type(self):
        return self._event_type

    @staticmethod
    def from_json(payload: any):
        """
        Build an object `BatteryStateChangeEvent` from the specified JSON
        expression.


        @param payload: JSON representation of a battery state change event::

            {
              "battery_level": decimal,
              "event_ref": string,
              "event_time": timestamp,
              "event_type": string,
              "location": {
                "accuracy": decimal,
                "altitude": decimal,
                "bearing": decimal,
                "fix_time": timestamp,
                "latitude": decimal,
                "longitude": decimal,
                "provider": string,
                "speed": decimal
              }
            }

            where:

            - `battery_level` (required): The level in percentage of the mobile
                device's battery (expressed between `0.0` and `1.1`) when this
                event occurred.

            - `event_ref` (required): The reference of this event as given by the
              client application running on the mobile device that reported this
              event.

              This information is used to detect events that the mobile device would
              report multiple times.  This happens when network outage occurs after
              the client application reported successfully a batch of events, but
              the network connection with the cloud service timed out before the
              client application had the chance to receive the acknowledgement from
              the cloud service.  Therefore, the client application reattempts to
              report one more time these events.

            - `event_time` (required): The time when this event occurred, which
              could be slightly different from the time when the device sent this
              event to the platform, for instance, in case of limited network
              connectivity, the device decided to cache locally this event before
              sending it eventually to the platform.

            - `event_type` (required): Indicate the type of event that occurred:

              - `battery_charging`: The level of the device's battery has
                increased significantly;

              - `battery_discharging`: The level of the device's battery has
                decreased significantly;

              - `battery_plugged`: The battery of the device has been plugged to
                a power source;

              - `battery_unplugged`: The battery of the device has been unplugged
                from a power source.

            - `location` (optional): Last known location of the device when this
              event occurred:

                  - `accuracy` (required): The accuracy in meters of the location.

                  - `altitude` (required): The altitude in meters of the location.

                  - `bearing` (optional): The bearing in degrees of the device.  Bearing
                    is the horizontal direction of travel of the device, and is not
                    related to the device orientation.  It is guaranteed to be in the
                    range `[0.0, 360.0]`.

                  - `fix_time` (required): The time when the device determined the
                    information of this location fix.

                  - `latitude` (required): The latitude-angular distance, expressed in
                    decimal degrees (WGS84 datum), measured from the center of the Earth,
                    of a point north or south of the Equator corresponding to the
                    location.

                  - `longitude` (required): The longitude-angular distance, expressed in
                    decimal degrees (WGS84 datum), measured from the center of the Earth,
                    of a point east or west of the Prime Meridian corresponding to the
                    location.

                  - `provider` (required): The code name of the location provider that
                    reported the location.

                    - `fused`: The location API in Google Play services that combines
                      different signals to provide the location information.

                    - `gps`: indicate that the location has been provided by a Global
                      Positioning System (GPS).

                    - `network`: indicate that the location has been provided by an hybrid
                      positioning system, which uses different positioning technologies,
                      such as Global Positioning System (GPS), Wi-Fi hotspots, cell tower
                      signals.

                    - `passive`: A special location provider for receiving locations without
                      actually initiating a location fix.  This provider can be used to
                      passively receive location updates when other applications or services
                      request them without actually requesting the locations yourself.  This
                      provider will return locations generated by other providers.

                  - `speed` (optional): The speed in meters/second over the ground.


        @return: an instance `BatteryStateChange`.
        """
        return payload and BatteryStateChangeEvent(
            payload['event_ref'],
            cast.string_to_enum(payload['event_type'], BatteryStateEventType),
            cast.string_to_timestamp(payload['event_time']),
            payload['battery_level'],
            location=GeoPoint.from_json(payload.get('location')))

    @property
    def location(self):
        return self._location


class LocationUpdate(Event):
    """
    Geographical location report that a mobile device sent to the
    Location-Based Service (LBS) platform.
    """
    def __eq__(self, other):
        """
        Indicate whether this location report object is the same as another
        location passed to this function.


        @param other: an instance `LocationUpdate`.


        @return: `True` if the two objects represent the same geographical
            location report (same identification and same fix time); `False`
            otherwise.
        """
        return 0 if self._event_ref == other.event_ref \
            else self._location.fix_time == other.location.fix_time

    def __init__(
            self,
            event_ref,
            event_time,
            location,
            mileage=None,
            network_type=None,
            payload=None,
            satellites=None):
        """
        Build a new instance `LocationUpdate`.


        @param event_ref: The reference of this event as given by the client
             application running on the mobile device that reported this event.

             This information is used to detect events that the mobile device would
             report multiple times.  This happens when network outage occurs after
             the client application reported successfully a batch of events, but
             the network connection with the cloud service timed out before the
             client application had the chance to receive the acknowledgement from
             the cloud service.  Therefore, the client application reattempts to
             report one more time these events.

        @param event_time: The time when this event occurred, which
             could be slightly different from the time when the device sent this
             event to the platform, for instance, in case of limited network
             connectivity, the device decided to cache locally this event before
             sending it eventually to the platform.

        @param location: The location fix reported by the mobile device.

        @param mileage: The total distance travelled by the mobile device
            since the application has been installed and executed on this
            device.  This mileage is calculated by the device itself based on
            the location changes its internal GPS determined over the time.

            This mileage might not correspond to the mileage displayed by the
            odometer of the vehicle this device is mounted on.

        @param network_type: A string representation of the network connection
            at the time this location fix has been determined by the mobile
            device of this location fix:

               MNCMCC:type[:subtype]

          where:

          - MNCMCC:string` (required): A Mobile Network Code (MNC) used in
            combination with a Mobile Country Code (MCC) (also known as a "MCC/MNC
            tuple") to uniquely identify the telephony operator of the mobile
            device.

          - `type:string` (required): A human-readable name that describes the
            type of the network that the device is connected to, such as `wifi`,
            `mobile`, `unknown`.

          - `subtype:string` (optional): A human-readable name that describes the
            subtype of this network when applicable.  Network of type `wifi` has
            no subtype.  Network of type `mobile` can have a subtype such as
            `egde`, `hsdpa`, etc.

        @param payload: A JSON expression of additional information that the
            mobile device provided within this report.

        @param satellites: A string representation of the information about
            the satellites that were used to calculate this location fix:

                (azimuth:elevation:PRN:SNR)[, ...]

            where:

            - `azimuth:float`: Azimuth of the satellite in degrees.

            - `elevation:float`: Elevation of the satellite in degrees.

            - `PRN:integer`: Pseudo-Random Number (PRN) for the satellite.

            - `SNR:float`: Signal to Noise Ratio (SNR) for the satellite.
        """
        super().__init__(event_ref, event_time)
        self._location = location
        self._network_type = network_type
        self._payload = payload
        self._satellites = satellites

    @staticmethod
    def from_json(payload):
        """
        Build a `LocationUpdate` object from the specified JSON object.


        @param payload: A JSON representation of a location report:

                {
                  "accuracy": decimal,
                  "altitude": decimal,
                  "bearing": decimal,
                  "event_ref": string,
                  "event_time": timestamp,
                  "fix_time": timestamp,
                  "latitude": decimal,
                  "longitude": decimal,
                  "mileage": decimal,
                  "network_type": string,
                  "provider": string,
                  "satellites": string,
                  "speed": decimal
                }

            where:

            - `accuracy` (required): The accuracy in meters of the location.

            - `altitude` (required): The altitude in meters of the location.

            - `bearing` (optional): The bearing in degrees of the mobile device.
              Bearing is the horizontal direction of travel of the mobile device,
              and is not related to the device orientation.  It is guaranteed to be
              in the range `[0.0, 360.0]`.

            - `event_ref` (required): The reference of this event as given by the
              client application running on the mobile device that reported this
              event.

              This information is used to detect events that the mobile device would
              report multiple times.  This happens when network outage occurs after
              the client application reported successfully a batch of events, but
              the network connection with the cloud service timed out before the
              client application had the chance to receive the acknowledgement from
              the cloud service.  Therefore, the client application reattempts to
              report one more time these events.

            - `event_time` (required): The time when this event occurred, which
              could be slightly different from the time when the device sent this
              event to the platform, for instance, in case of limited network
              connectivity, the device decided to cache locally this event before
              sending it eventually to the platform.

            - `fix_time` (required): The time when the mobile device determined
              the information of this fix.

            - `latitude` (required): The latitude-angular distance, expressed in
              decimal degrees (WGS84 datum), measured from the center of the Earth,
              of a point north or south of the Equator.

            - `longitude` (required): The longitude-angular distance, expressed in
              decimal degrees (WGS84 datum), measured from the center of the Earth,
              of a point east or west of the Prime Meridian.

            - `network_type` (optional): String representation of the network
              connection at the time this geographical location fix has been
              determined by the mobile device:

                  MNCMCC:type[:subtype]

              where:

              - `MNCMCC:string` (required): A Mobile Network Code (MNC) used in
                combination with a Mobile Country Code (MCC) (also known as a "MCC/MNC
                tuple") to uniquely identify the telephony operator of the mobile
                device.

              - `type:string` (required): A human-readable name that describes the
                type of the network that the device is connected to, such as `wifi`,
                `mobile`, `unknown`.

              - `subtype:string` (optional): A human-readable name that describes the
                subtype of this network when applicable.  Network of type `wifi` has
                not subtype.  Network of type `mobile` can have a subtype such as
                `egde`, `hsdpa`, etc.

            - `payload` (optional): JSON expression of additional information that
              the mobile device provided within this report.

            - `provider` (required): The type of the location provider that reported
              the location such as:

              - `fused`: The location API in Google Play services that combines
                different signals to provide the location information.

              - `gps`: This provider determines location using satellites.

              - `network`: This provider determines location based on availability of
                cell towers and Wi-Fi access points.  Results are retrieved by means
                of a network lookup.

              - `passive`: A special location provider for receiving locations without
                actually initiating a location fix.  This provider can be used to
                passively receive location updates when other applications or services
                request them without actually requesting the locations yourself.  This
                provider will return locations generated by other providers.

            - `satellites` (optional): A string representation of the information
              about the satellites that were used to calculate this location fix:

                  (azimuth:elevation:PRN:SNR)[, ...]

              where:

              - `azimuth:float`: The azimuth of the satellite in degrees.

              - `elevation:float`: The elevation of the satellite in degrees.

              - `PRN:integer`: The Pseudo-Random Number (PRN) for the satellite.

              - `SNR:float`: The signal to Noise Ratio (SNR) for the satellite.

            * `speed` (optional): Speed in meters/second over the ground.


        @return: A `LocationUpdate` object.
        """
        return payload and LocationUpdate(
            payload['event_ref'],
            cast.string_to_timestamp(payload['event_time']),
            GeoPoint(
                payload['latitude'],
                payload['longitude'],
                accuracy=payload['accuracy'],  # Required for tracked location
                altitude=payload['altitude'],  # Required for tracked location
                bearing=payload.get('bearing'),
                fix_time=cast.string_to_timestamp(payload['fix_time']),  # Required for tracked location
                provider=payload['provider'],  # Required for tracked location
                speed=payload.get('speed')),
            network_type=payload.get('network_type'),
            payload=payload.get('payload'),
            satellites=payload.get('satellites'))

    @property
    def location(self):
        return self._location

    @property
    def network_type(self):
        return  self._network_type

    @property
    def payload(self):
        return self._payload

    @property
    def satellites(self):
        return self._satellites
