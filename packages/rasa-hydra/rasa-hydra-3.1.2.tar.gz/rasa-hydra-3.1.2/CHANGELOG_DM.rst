:desc: Rasa-Hydra Changelog

Rasa-Hydra Change Log
=====================

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning`_ starting with version 1.0.

[3.1.2] - [Unreleased]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Log cdr submissions as warning
- Update default config cdr url env name default

[3.1.1] - [Unreleased]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Converted redis calls to async 

[3.1.0] - [Unreleased]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Log asr engine as part of app nav label

[3.0.5] - [Unreleased]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Add AIOKafka broker.

[3.0.4] - [Unreleased]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Update 3.x testing and appNav submission patch

[3.0.3] - [Unreleased]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Fix app nav submission

[3.0.2] - [Unreleased]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Fix clear_model_files event listener on shutdown

[3.0.1] - [Unreleased]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- refactor load_agent function so interpreter does not default to english for both agents

[3.0.0] - [Unreleased]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Rasa handles multiple agents based on session language (MVP)

[2.6.66] - [unreleased]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Fix app nav NLU submission

[2.6.65] - [unreleased]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Move environment variable access into single file for imports.

[2.6.64] - [unreleased]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- refactor message to digit conversion for redacted data logged to tracker

[2.6.63] - [unreleased]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Add new arguments for Kafka producer to reduce latency.

[2.6.62] - [unreleased]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Update redaction process to completely mask invalid input for no_match grammar events

[2.6.61] - 2022-03-01
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Add spanish digit redaction rules

[2.6.60] - 2022-02-18
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Add error handling for text-to-digit redaction

[2.6.59] - [Unreleased]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Re-enable App Nav submission to Freeclimb

[2.6.58] - 2022-02-18
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Remove Volatage library

[2.6.57] - 2022-02-18
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Removed App Nav submissions to Freeclimb

[2.6.56] - 2022-02-18
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Fix string redaction logic for spaced digits

Changed
-------
- Make app nav submission asynchronous 

[2.6.55] - 2022-02-16
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- log app_nave results for NLU match, no_match, and disconnect events
- log app_nav results in prometheus

[2.6.54] - 2022-01-04
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Added injection of "language" attribute to templates

[2.6.53] - 2021-12-02
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Health checks updated to prevent cascading failures

[2.6.52] - 2021-09-28
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Make empty message condition stricter for steps count.

[2.6.51] - 2021-09-01
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- TEMPORARY FIX: Return channel id env variable, remove omni-api

[2.6.50] - 2021-08-17
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Fix add conversation steps conditions to account for app events, disconnect events, and empty user messages.

[2.6.49] - 2021-08-17
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Change total steps count conditions to meet new requirements.

[2.6.48] - 2021-08-17
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Add step number to events.

[2.6.47] - 2021-08-09
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Omit redaction on disconnect event

[2.6.46] - 2021-08-09
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Omit sip events when tracking last BotResponse

[2.6.45] - 2021-07-28
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- change special words to digit values for better redaction default

[2.6.44] - 2021-07-28
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- refactor rasa processor redaction for speech message types

[2.6.43] - 2021-07-27
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- redact rasa processor logging

[2.6.42] - 2021-07-27
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- refactor metadata redaction when privacy_mode is true (use redact_generic_strict)

[2.6.41] - 2021-07-26
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- omit punction removal of special dtmf/punctuation inputs when converting text-to-digits

[2.6.40] - 2021-07-22
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Root logger redaction rules
Fixed
-------
- Redaction strategy moved from message to broker


[2.6.39] - 2021-07-22
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- change default redaction rule (digit_length > 10)
- omit redaction on initial /greet condition

[2.6.38] - 2021-07-15
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Add condition to exclude injected user messages from steps count.

Fixed
-------
- change default redaction rule (digit_length > 10)

[2.6.37] - 2021-06-26
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- add grammarfile to tracker-consumer metadata

[2.6.36] - 2021-06-26
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- redact parse_data text value

[2.6.35] - 2021-06-26
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Fix default redaction punctuation bug

[2.6.34] - 2021-06-25
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Fix default redaction bug

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[2.6.33] - 2021-06-24
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Add group name to metadata.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[2.6.32] - 2021-15-21
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Fixed redaction functions to partials and original text

[2.6.31] - 2021-05-21
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Added original_text and partials to metadata

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[2.6.31] - 2021-05-21
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- update default redaction for cc values passed accross entites

[2.6.30] - 2021-05-21
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Fixed template prompt name passed on fallback

[2.6.29] - 2021-05-21
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Fixed startTracking() method to properly append guid to existing slots
Changed
-------
- Partials strategy conditional to accommodate NoneType

[2.6.28] - 2021-05-20
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Partials strategy
- Remove cert verification from omni-api request

[2.6.26] - 2021-04-08
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------

- Redactor redaction process based on privacy mode boolean
- Redact all 13,15,16, or 19 digit numbers regardless of privacy mode

[2.6.24] - 2021-04-08
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------

- Fix issue of not extracting custom nlu threshold from custom policy


[2.6.23] - 2021-04-05
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------

- Remove Kafka broker health check.
- Remove UPM health check.


[2.6.22] - 2021-03-21
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------

- Move Kafka health check to a different thread

[2.6.21] - 2021-03-21
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------

- Set Kafka Producer acks to 1.


[2.6.20] - 2021-03-16
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------

- Set reinitialize_steps to 1

[2.6.18] - 2021-03-16
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------

- More bugs fix in the Redis tracker store.


[2.6.15] - 2021-03-16
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------

- Add retry logic in the RedisClusterTrackerStore.


[2.6.14] - 2021-03-16
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------

- Handle the case where channelId equals to 0


[2.6.13] - 2021-03-10
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------

- Refactor fields used in the metadata of user messages


[2.6.12] - 2021-03-9
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------

- Fetch channel id when the app first loads


[2.6.11] - 2021-03-8
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------

- Add user message redaction for user and database logging
- Refactor aiohttp client session in the readiness check

[2.6.9] - 2021-02-22
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------

- Add nlu file and version endpoint
- Include metadata in the parse_data of the UserUttered event.


[2.6.8] - 2021-02-22
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------

- Set TTL of Redis trackers to 1 hour for voice channels and 2 hours for everything else.


[2.6.7] - 2021-02-21
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------

- Add outcome slot after getting the /disconnect trigger from tracker-ttl-manager

[2.6.6] - 2021-02-18
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Remove the hardcoded 20 mins TTL for the voice channel.


[2.6.5] - 2021-02-12
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Increase the default ducking requests timeout to 30s
- Fix the issue of the health check endpoint not reporting failure in connecting to the tracker store.

[2.6.4] - 2021-02-03
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Reuse aiohttp client session in the ducklingHTTPExtractor to improve its performance.
- Added a new endpoint to check if a tracker exists in the tracker store.

[2.6.4a2]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Reuse aiohttp client session in the ducklingHTTPExtractor to improve its performance.

[2.6.4a1]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Added a new endpoint to check if a tracker exists in the tracker store.

[2.6.3]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Collect confidenceThreshold from the templates in the domain file.
- Fix the connection reset error in using the same aiohttp session.


[2.6.2]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Add asrThreshold and nluThreshold to the metadata of each user message
- Changed should add condition for empty input scenerio
- Fix incorrect tracker store healthy check in the FailSafeTrackerStore
- Fix the issue with not handling the events after the disconnect message in the core processor.
- Skip adding disconnect events to the tracker if the conversation has been ended.
- Fix some issues with appending the disconnect event in the SQL tracker store.
- Pin the version of python-socketio to be < 5.x
- Include db schema in the queries used by the SQL tracker store
- Add MSSQL tracker store
- Add error message to metadata
- Better error descriptions in healthcheck failures

[2.6.2a8]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Add asrThreshold and nluThreshold to the metadata of each user message

[2.6.rc9]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Changed should add condition for empty input scenerio

[2.6.2a7]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Fix incorrect tracker store healthy check in the FailSafeTrackerStore

[2.6.2a6]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Fix the issue with not handling the events after the disconnect message in the core processor.

[2.6.2a5]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Skip adding disconnect events to the tracker if the conversation has been ended.

[2.6.2a4]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Fix some issues with appending the disconnect event in the SQL tracker store.

[2.6.2a3]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Pin the version of python-socketio to be < 5.x

[2.6.2a2]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Include db schema in the queries used by the SQL tracker store

[2.6.2a1]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Add MSSQL tracker store

[2.6.2c]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Add error message to metadata

[2.6.2a]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Better error descriptions in healthcheck failures

[2.6.1] - `master`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Fix tracker ttl timeout
- Append system disconnect event if the tracker object expired
- Refactor codes to calculate the total steps of the conversation
- Set default 20 mins ttl for the users from the voice channel
- Skip saving the tracker objects again after events are received from the tracker-ttl-manager
- Include types of error in the metadata of the bot messages.
- Fix the issue with starting interactive mode
- Only stream errors and steps to the event broker when the conversation has ended
- Convert Kafka broker url into a list if it's separated by commas
- Add MSSQL support for the tracker stores

[2.6.0a13]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Add MSSQL support for the tracker stores

[2.6.0a12]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Convert Kafka broker url into a list if it's separated by commas

[2.6.0a11]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Only stream errors and steps to the event broker when the conversation has ended

[2.6.0a6]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Fix the issue with starting interactive mode

[2.6.0a5]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Include types of error in the metadata of the bot messages.

[2.6.0a4]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Skip saving the tracker objects again after events are received from the tracker-ttl-manager


[2.6.0a3]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Set default 20 mins ttl for the users from the voice channel

[2.6.0a2]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Append system disconnect event if the tracker object expired
- Refactor codes to calculate the total steps of the conversation

[2.6.0a1]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Fix tracker ttl timeout

[2.6.0]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Upgrade rasa to 1.5.3

[2.5.8a11]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Fix the issue with trying to convert None into lowercase.

[2.5.8a10]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Keep track of the total steps and errors of each conversation.

[2.5.8a9]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Measure time taken of Redis get and set
- Measure time taken of sending sending to Kafka

[2.5.8a7]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Use perf_counter() instead of time().

[2.5.8a6]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Update the default ttl value to 2 mins for the voice channel and 2 hours for everything else.

[2.5.8a3]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Don't save the trackers into the tracker store again when a "/disconnect" message is received through an endpoint

[2.5.8a2]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Make endpoint as an optional arg of create_http_input_channels

[2.5.8a1]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Add idp and upm as a part of the readiness health check.

[2.5.7a14]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Add messageType to metadata

[2.5.7a13]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Add json-logging to allow logs in the JSON format

[2.5.7a11]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Remove retry logic for the requests to the remote action server

[2.5.7a9]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Change the logging level for the errors of the remote action requests to ERROR

[2.5.7a8] - `develop`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Log application messages in the JSON format

[2.5.7a7]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Retry the request to the action server once if asyncio.CancelledError occurs

[2.5.7a6]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Include sender_id in the error logs from executing actions
- Set some default values for the uri of and tenant id for IDP

[2.5.7a5]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Pass Tenant-Id as part of startTracking IdP request header

[2.5.7a4]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Record the time taken of remote actions to be finished in the metric endpoint.

[2.5.7a3]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Fix the http_status in the metrics for the rasa-duckling requests.

[2.5.7a2]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Insert the values into the variables used in the custom audio filename

[2.5.7a1]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Added active_handoff metadata to messages.

[2.5.7a0]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Fix the issue of calling the run_evaluation method without awaiting it and some unit tests

[2.5.7]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Modified logic for marking LiveChat messages
- Modified missedIntent logic to skip LiveChat messages

[2.5.6]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Modified agent/response endpoint to initiate action_listen after agent 
    disconnect
- Updated processor to attach handoff_active metadata to bot messages

[2.5.5]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Implemented AsyncRedisManager for handling cross-process socketio
    communication.
- Updated requirements to include aiohttp module, as it
    is necessary for utilizing the AsyncRedisManager 
    class

[2.5.4]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Fixed live_chat_policy to properly handle disconnect

[2.5.3]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fixed
-------
- Fixed parsing error in /agent/response callback function

[2.5.2]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Added agent/response CallBack endpoint for live chat support webhooks
- Added _get_output_channel_without_request function to retrieve output
    channel when triggered by CallBack.

[2.5.1]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Measure time taken for the requests to rasa-duckling

[2.5.0]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Expose prometheus metrics for each endpoint

[2.4.0]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Revert async changes in the tracker stores

[2.3.0]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Replace request with aiohttp in the DucklingHTTPExtractor

[2.2.7]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Change the logging level of health check endpoints to DEBUG

[2.2.6]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Log time taken for duckling and remote actions

[2.2.5]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Log predicted actions with their confidences

[2.2.4]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Filter user pii data by checking if the filling slot starts with 'confidential'

[2.2.3]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Simply upgrade the version without any code change

[1.2.1]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Terminate user active sessions before shutting down the server

[1.2.0]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Return the original user message if the request to IDP has failed

[1.1.0]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Modify user greeting message in the startTracking method

[1.0.0]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Major version update without any code change

[0.2.5a2]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Stream events to brokers even though csi is not set

[0.2.5a1]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Extract the type of the user message and add it into the metadata


[0.2.4]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Fix issues of mixing metadata with parse_data

[0.2.3]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Fix buttons issues in the FB channel

Added
-----
- Add metadata for user messages

[0.2.2]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-------
- Add health check for event brokers
- Create a system event when users disconnect

Changed
-------
- Fix broken Rasa unit tests
- Revert aiohttp changes in the duckling extractor
- Updated missed_intent logic to bypass form inputs

[0.2.1]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-----
- Publish NLU events to the event broker
- ParseList endpoint

Changed
-------
- Update the readiness check to allow nlu only
- Fix interactive training issues
- Fix missing dependencies for installing rasa-hydra

Removed
-------
- Remove old training data

[0.2.0]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Updated Rasa from 1.1.8 to 1.2.3
- Fixed asyncio issue within NLU evaluation flow

[0.1.2]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Added
-----
- Added changelog for the rasa-hydra project.

Changed
-------
- Updated README.md to include development and release information for Rasa-Hydra.
- Updated setup.py to include the Hydra team.

[0.1.1]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Upgraded Rasa to 1.1.8.

[0.1.0]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
-------
- Updated codes to work with the Hydra chatbot.

Removed
-------
- Removed codes and the model file for running the Hydra chatbot.

.. _`master`: https://gitlab.vailsys.com/CueAi/rasa/
.. _`develop`: https://gitlab.vailsys.com/CueAi/rasa/tree/develop

.. _`Semantic Versioning`: http://semver.org/
