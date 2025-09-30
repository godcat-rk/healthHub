# Oura API ???????

Oura API v2 ??? OpenAPI ?? (openapi-1.27) ?????healthHub ????????????????????????????????????
???????????????????????????????????????????????????

## ???????????
???? | ??????? | ?????? | ???????
|-|-|-|-|
?????? | `/v2/usercollection/daily_sleep` | Multiple Daily Sleep Documents | ??????????????????????????????????????
????? | `/v2/usercollection/sleep` | Multiple Sleep Documents | 1 ?????????????????????????HRV???????
?????? | `/v2/usercollection/daily_readiness` | Multiple Daily Readiness Documents | ???????????????????????????
?????? | `/v2/usercollection/daily_activity` | Multiple Daily Activity Documents | ?????????????????????????????
????? | `/v2/usercollection/workout` | Multiple Workout Documents | ??????????????????????????????????????
????? | `/v2/usercollection/session` | Multiple Session Documents | ?????????????????????????????????????
?????? | `/v2/usercollection/daily_stress` | Multiple Daily Stress Documents | ????????????????????????????????
?????? | `/v2/usercollection/daily_resilience` | Multiple Daily Resilience Documents | ?????????????????????????????
?????? | `/v2/usercollection/daily_cardiovascular_age` | Multiple Daily Cardiovascular Age Documents | ???????????????????????????????????????
?????? | `/v2/usercollection/daily_spo2` | Multiple Daily Spo2 Documents | ?? SpO? ?????????????????????????????????
???? | `/v2/usercollection/vO2_max` | Multiple Vo2 Max Documents | ?????????????????????????????????
?????? | `/v2/usercollection/heartrate` | Multiple Heart Rate Documents | 5 ????????????????????????????
?????? | `/v2/usercollection/sleep_time` | Multiple Sleep Time Documents | ???????????????????????????????
????? | `/v2/usercollection/tag` | Multiple Tag Documents | ????????????????????????????????
????? | `/v2/usercollection/enhanced_tag` | Multiple Enhanced Tag Documents | ?????????????????????????????
????? | `/v2/usercollection/personal_info` | Single Personal Info Document | ????????????????????????
????? | `/v2/usercollection/ring_configuration` | Multiple Ring Configuration Documents | ??????????????????????????
????? | `/v2/usercollection/rest_mode_period` | Multiple Rest Mode Period Documents | ???????????????????????????????????

## ???????? ? `/v2/usercollection/daily_sleep`
- **??**: ??????????????????????????????????????
- **??????**: Multiple Daily Sleep Documents
- **????????**: `DailySleepModel`
- **??????**:
  - `score` [integer | null]: Daily sleep score.
  - `contributors.total_sleep` [integer | null]: Contribution of total sleep in range [1, 100].
  - `contributors.restfulness` [integer | null]: Contribution of sleep restfulness in range [1, 100].
  - `contributors.efficiency` [integer | null]: Contribution of sleep efficiency in range [1, 100].

### ???????
????? | ? | ????
|-|-|-|
`id` | string | Id
`contributors` | SleepContributors | Contributors for the daily sleep score.
`contributors.deep_sleep` | integer | null | Contribution of deep sleep in range [1, 100].
`contributors.efficiency` | integer | null | Contribution of sleep efficiency in range [1, 100].
`contributors.latency` | integer | null | Contribution of sleep latency in range [1, 100].
`contributors.rem_sleep` | integer | null | Contribution of REM sleep in range [1, 100].
`contributors.restfulness` | integer | null | Contribution of sleep restfulness in range [1, 100].
`contributors.timing` | integer | null | Contribution of sleep timing in range [1, 100].
`contributors.total_sleep` | integer | null | Contribution of total sleep in range [1, 100].
`day` | string | Day that the daily sleep belongs to.
`score` | integer | null | Daily sleep score.
`timestamp` | LocalDateTime | Timestamp of the daily sleep.

## ????????? ? `/v2/usercollection/sleep`
- **??**: 1 ?????????????????????????HRV???????
- **??????**: Multiple Sleep Documents
- **????????**: `SleepModel`
- **??????**:
  - `total_sleep_duration` [integer | null]: Total sleep duration in seconds.
  - `deep_sleep_duration` [integer | null]: Duration spent in deep sleep in seconds.
  - `rem_sleep_duration` [integer | null]: Duration spent in REM sleep in seconds.
  - `lowest_heart_rate` [integer | null]: Lowest heart rate during sleep.
  - `average_hrv` [integer | null]: Average heart rate variability during sleep.

### ???????
????? | ? | ????
|-|-|-|
`id` | string | Id
`average_breath` | number | null | Average breathing rate during sleep as breaths/second.
`average_heart_rate` | number | null | Average heart rate during sleep as beats/minute.
`average_hrv` | integer | null | Average heart rate variability during sleep.
`awake_time` | integer | null | Duration spent awake in seconds.
`bedtime_end` | LocalDateTime | Bedtime end of the sleep.
`bedtime_start` | LocalDateTime | Bedtime start of the sleep.
`day` | string | Day that the sleep belongs to.
`deep_sleep_duration` | integer | null | Duration spent in deep sleep in seconds.
`efficiency` | integer | null | Sleep efficiency rating in range [1, 100].
`heart_rate` | SampleModel | null | Object containing heart rate samples.
`hrv` | SampleModel | null | (????)
`latency` | integer | null | Sleep latency in seconds. This is the time it took for the user to fall asleep after going to bed.
`light_sleep_duration` | integer | null | Duration spent in light sleep in seconds.
`low_battery_alert` | boolean | Flag indicating if a low battery alert occurred.
`lowest_heart_rate` | integer | null | Lowest heart rate during sleep.
`movement_30_sec` | string | null |          30-second movement classification for the period where every character corresponds to:         '1' = no motion,         '2' = restless,         '3' = tossing and turning         '4' = active         
`period` | integer | ECore sleep period identifier.
`readiness` | ReadinessSummary | null | Object containing the readiness details for this sleep. As opposed to the daily readiness object which represents the readiness for the entire day.
`readiness_score_delta` | integer | null | Effect on readiness score caused by this sleep period.
`rem_sleep_duration` | integer | null | Duration spent in REM sleep in seconds.
`restless_periods` | integer | null | Number of restless periods during sleep.
`sleep_phase_5_min` | string | null |          5-minute sleep phase classification for the period where every character corresponds to:         '1' = deep sleep,         '2' = light sleep,         '3' = REM sleep         '4' = awake.         
`sleep_score_delta` | integer | null | Effect on sleep score caused by this sleep period.
`sleep_algorithm_version` | SleepAlgorithmVersion | null | Version of the sleep algorithm used to calculate the sleep data.
`sleep_analysis_reason` | SleepAnalysisReason | null | The reason for the creation or update of the latest version of this sleep.
`time_in_bed` | integer | Duration spent in bed in seconds.
`total_sleep_duration` | integer | null | Total sleep duration in seconds.
`type` | SleepType | (????)

## ??????????? ? `/v2/usercollection/daily_readiness`
- **??**: ???????????????????????????
- **??????**: Multiple Daily Readiness Documents
- **????????**: `DailyReadinessModel`
- **??????**:
  - `score` [integer | null]: Daily readiness score.
  - `temperature_deviation` [number | null]: Temperature deviation in degrees Celsius.
  - `contributors.recovery_index` [integer | null]: Contribution of recovery index in range [1, 100].
  - `contributors.resting_heart_rate` [integer | null]: Contribution of resting heart rate in range [1, 100].

### ???????
????? | ? | ????
|-|-|-|
`id` | string | Id
`contributors` | ReadinessContributors | Contributors of the daily readiness score.
`contributors.activity_balance` | integer | null | Contribution of cumulative activity balance in range [1, 100].
`contributors.body_temperature` | integer | null | Contribution of body temperature in range [1, 100].
`contributors.hrv_balance` | integer | null | Contribution of heart rate variability balance in range [1, 100].
`contributors.previous_day_activity` | integer | null | Contribution of previous day's activity in range [1, 100].
`contributors.previous_night` | integer | null | Contribution of previous night's sleep in range [1, 100].
`contributors.recovery_index` | integer | null | Contribution of recovery index in range [1, 100].
`contributors.resting_heart_rate` | integer | null | Contribution of resting heart rate in range [1, 100].
`contributors.sleep_balance` | integer | null | Contribution of sleep balance in range [1, 100].
`day` | string | Day that the daily readiness belongs to.
`score` | integer | null | Daily readiness score.
`temperature_deviation` | number | null | Temperature deviation in degrees Celsius.
`temperature_trend_deviation` | number | null | Temperature trend deviation in degrees Celsius.
`timestamp` | LocalDateTime | Timestamp of the daily readiness.

## ????????????? ? `/v2/usercollection/daily_activity`
- **??**: ?????????????????????????????
- **??????**: Multiple Daily Activity Documents
- **????????**: `DailyActivityModel`
- **??????**:
  - `score` [integer | null]: Activity score in range ```[1, 100]```
  - `steps` [integer]: Total number of steps taken
  - `total_calories` [integer]: Total calories expended (in kilocalories)
  - `active_calories` [integer]: Active calories expended (in kilocalories)
  - `equivalent_walking_distance` [integer]: Equivalent walking distance (in meters) of energy expenditure

### ???????
????? | ? | ????
|-|-|-|
`id` | string | Id
`class_5_min` | string | null | 5-minute activity classification for the activity period: * ```0```	non wear * ```1``` rest * ```2``` inactive * ```3``` low activity * ```4``` medium activity * ```5``` high activity
`score` | integer | null | Activity score in range ```[1, 100]```
`active_calories` | integer | Active calories expended (in kilocalories)
`average_met_minutes` | number | Average metabolic equivalent (MET) in minutes
`contributors` | ActivityContributors | (????)
`contributors.meet_daily_targets` | integer | null | Contribution of meeting previous 7-day daily activity targets in range [1, 100].
`contributors.move_every_hour` | integer | null | Contribution of previous 24-hour inactivity alerts in range [1, 100].
`contributors.recovery_time` | integer | null | Contribution of previous 7-day recovery time in range [1, 100].
`contributors.stay_active` | integer | null | Contribution of previous 24-hour activity in range [1, 100].
`contributors.training_frequency` | integer | null | Contribution of previous 7-day exercise frequency in range [1, 100].
`contributors.training_volume` | integer | null | Contribution of previous 7-day exercise volume in range [1, 100].
`equivalent_walking_distance` | integer | Equivalent walking distance (in meters) of energy expenditure
`high_activity_met_minutes` | integer | High activity metabolic equivalent (MET) in minutes
`high_activity_time` | integer | High activity metabolic equivalent (MET) in seconds
`inactivity_alerts` | integer | Number of inactivity alerts received
`low_activity_met_minutes` | integer | Low activity metabolic equivalent (MET) in minutes
`low_activity_time` | integer | Low activity metabolic equivalent (MET) in seconds
`medium_activity_met_minutes` | integer | Medium activity metabolic equivalent (MET) in minutes
`medium_activity_time` | integer | Medium activity metabolic equivalent (MET) in seconds
`met` | SampleModel | (????)
`met.interval` | number | Interval in seconds between the sampled items.
`met.items` | array<object> | Recorded sample items.
`met.timestamp` | LocalDateTimeWithMilliseconds | Timestamp when the sample recording started.
`meters_to_target` | integer | Remaining meters to target (from ```target_meters```
`non_wear_time` | integer | The time (in seconds) in which the ring was not worn
`resting_time` | integer | Resting time (in seconds)
`sedentary_met_minutes` | integer | Sedentary metabolic equivalent (MET) in minutes
`sedentary_time` | integer | Sedentary metabolic equivalent (MET) in seconds
`steps` | integer | Total number of steps taken
`target_calories` | integer | Daily activity target (in kilocalories)
`target_meters` | integer | Daily activity target (in meters)
`total_calories` | integer | Total calories expended (in kilocalories)
`day` | string | The ```YYYY-MM-DD``` formatted local date indicating when the daily activity occurred
`timestamp` | LocalDateTime | ISO 8601 formatted local timestamp indicating the start datetime of when the daily activity occurred

## ??????????? ? `/v2/usercollection/workout`
- **??**: ??????????????????????????????????????
- **??????**: Multiple Workout Documents
- **????????**: `PublicWorkout`
- **??????**:
  - `calories` [number | null]: Energy burned in kilocalories during the workout.
  - `distance` [number | null]: Distance traveled in meters during the workout.
  - `heart_rate.average`: (field not found in schema)
  - `intensity` [PublicWorkoutIntensity]: Intensity of the workout.
  - `class`: (field not found in schema)

### ???????
????? | ? | ????
|-|-|-|
`id` | string | Unique identifier of the object.
`activity` | string | Type of the workout activity.
`calories` | number | null | Energy burned in kilocalories during the workout.
`day` | ISODate | Day when the workout occurred.
`distance` | number | null | Distance traveled in meters during the workout.
`end_datetime` | LocalizedDateTime | Timestamp indicating when the workout ended.
`intensity` | PublicWorkoutIntensity | Intensity of the workout.
`label` | string | null | User-defined label for the workout.
`source` | PublicWorkoutSource | Possible workout sources.
`start_datetime` | LocalizedDateTime | Timestamp indicating when the workout started.

## ??????????? ? `/v2/usercollection/session`
- **??**: ?????????????????????????????????????
- **??????**: Multiple Session Documents
- **????????**: `SessionModel`
- **??????**:
  - `state`: (field not found in schema)
  - `mood` [MomentMood | null]: (????)
  - `duration`: (field not found in schema)
  - `heart_rate.average`: (nested field not resolved)
  - `temperature`: (field not found in schema)

### ???????
????? | ? | ????
|-|-|-|
`id` | string | Id
`day` | string | The date when the session occurred.
`start_datetime` | LocalDateTime | Timestamp indicating when the Moment ended.
`end_datetime` | LocalDateTime | Timestamp indicating when the Moment ended.
`type` | MomentType | (????)
`heart_rate` | SampleModel | null | (????)
`heart_rate_variability` | SampleModel | null | (????)
`mood` | MomentMood | null | (????)
`motion_count` | SampleModel | null | (????)

## ?????? ? `/v2/usercollection/daily_stress`
- **??**: ????????????????????????????????
- **??????**: Multiple Daily Stress Documents
- **????????**: `DailyStressModel`
- **??????**:
  - `stress_score`: (field not found in schema)
  - `stress_duration`: (field not found in schema)
  - `recovery_duration`: (field not found in schema)
  - `daytime_stress_duration`: (field not found in schema)

### ???????
????? | ? | ????
|-|-|-|
`id` | string | Id
`day` | string | Day that the daily stress belongs to.
`stress_high` | integer | null | Time (in seconds) spent in a high stress zone (top quartile data)
`recovery_high` | integer | null | Time (in seconds) spent in a high recovery zone (bottom quartile data)
`day_summary` | DailyStressSummary | null | Stress summary of full day.

## ???????? ? `/v2/usercollection/daily_resilience`
- **??**: ?????????????????????????????
- **??????**: Multiple Daily Resilience Documents
- **????????**: `DailyResilienceModel`
- **??????**:
  - `resilience_score`: (field not found in schema)
  - `state`: (field not found in schema)
  - `contributors.strain`: (field not found in schema)
  - `contributors.recovery`: (field not found in schema)

### ???????
????? | ? | ????
|-|-|-|
`id` | string | Id
`day` | string | Day when the resilience record was recorded.
`contributors` | ResilienceContributors | Contributors to the resilience score.
`contributors.sleep_recovery` | number | Sleep recovery contributor to the resilience score. Range: [0, 100]
`contributors.daytime_recovery` | number | Daytime recovery contributor to the resilience score. Range: [0, 100]
`contributors.stress` | number | Stress contributor to the resilience score. Range: [0, 100]
`level` | LongTermResilienceLevel | Resilience level.

## ??????? ? `/v2/usercollection/daily_cardiovascular_age`
- **??**: ???????????????????????????????????????
- **??????**: Multiple Daily Cardiovascular Age Documents
- **????????**: `DailyCardiovascularAgeModel`
- **??????**:
  - `age`: (field not found in schema)
  - `age_vs_chronological`: (field not found in schema)
  - `category`: (field not found in schema)

### ???????
????? | ? | ????
|-|-|-|
`day` | string | Day
`vascular_age` | integer | null | 'Predicted vascular age in range [18, 100].

## ?? SpO? ? `/v2/usercollection/daily_spo2`
- **??**: ?? SpO? ?????????????????????????????????
- **??????**: Multiple Daily Spo2 Documents
- **????????**: `DailySpO2Model`
- **??????**:
  - `spo2_percentage.average`: (nested field not resolved)
  - `breathing_disturbance_index` [integer | null]: Breathing Disturbance Index (BDI) calculated using detected SpO2 drops from timeseries. Values should be in range [0, 100]

### ???????
????? | ? | ????
|-|-|-|
`id` | string | Id
`day` | string | Day
`spo2_percentage` | DailySpO2AggregatedValuesModel | null | The SpO2 percentage value aggregated over a single day.
`breathing_disturbance_index` | integer | null | Breathing Disturbance Index (BDI) calculated using detected SpO2 drops from timeseries. Values should be in range [0, 100]

## ?? VO? Max ? `/v2/usercollection/vO2_max`
- **??**: ?????????????????????????????????
- **??????**: Multiple Vo2 Max Documents
- **????????**: `VO2MaxModel`
- **??????**:
  - `vo2_max` [number | null]: VO2 max value.
  - `lower_bound`: (field not found in schema)
  - `upper_bound`: (field not found in schema)

### ???????
????? | ? | ????
|-|-|-|
`id` | string | Id
`day` | string | Day that the estimate belongs to.
`timestamp` | LocalDateTime | Timestamp indicating when the estimate was created.
`vo2_max` | number | null | VO2 max value.

## ????? ? `/v2/usercollection/heartrate`
- **??**: 5 ????????????????????????????
- **??????**: Multiple Heart Rate Documents
- **????????**: `HeartRateModel`
- **??????**:
  - `bpm` [integer]: Bpm
  - `source` [HeartRateSource]: (????)
  - `timestamp` [LocalDateTime]: (????)

### ???????
????? | ? | ????
|-|-|-|
`bpm` | integer | Bpm
`source` | HeartRateSource | (????)
`timestamp` | LocalDateTime | (????)

## ??????? ? `/v2/usercollection/sleep_time`
- **??**: ???????????????????????????????
- **??????**: Multiple Sleep Time Documents
- **????????**: `SleepTimeModel`
- **??????**:
  - `bedtime_window`: (field not found in schema)
  - `status` [SleepTimeStatus | null]: Sleep time status; used to inform sleep time recommendation.
  - `optimal_bedtime` [SleepTimeWindow | null]: Optimal bedtime.
  - `recommendation_type`: (field not found in schema)

### ???????
????? | ? | ????
|-|-|-|
`id` | string | Id
`day` | string | Corresponding day for the sleep time.
`optimal_bedtime` | SleepTimeWindow | null | Optimal bedtime.
`recommendation` | SleepTimeRecommendation | null | Recommended action for bedtime.
`status` | SleepTimeStatus | null | Sleep time status; used to inform sleep time recommendation.

## ?????? ? `/v2/usercollection/tag`
- **??**: ????????????????????????????????
- **??????**: Multiple Tag Documents
- **????????**: `TagModel`
- **??????**:
  - `label`: (field not found in schema)
  - `day` [string]: Day that the note belongs to.
  - `notes`: (field not found in schema)
  - `tag_type`: (field not found in schema)

### ???????
????? | ? | ????
|-|-|-|
`id` | string | Id
`day` | string | Day that the note belongs to.
`text` | string | null | Textual contents of the note.
`timestamp` | LocalDateTime | Timestamp of the note.
`tags` | array<string> | Selected tags for the tag.

## ???? ? `/v2/usercollection/enhanced_tag`
- **??**: ?????????????????????????????
- **??????**: Multiple Enhanced Tag Documents
- **????????**: `EnhancedTagModel`
- **??????**:
  - `tag`: (field not found in schema)
  - `source`: (field not found in schema)
  - `items.name`: (field not found in schema)
  - `items.value`: (field not found in schema)

### ???????
????? | ? | ????
|-|-|-|
`id` | string | Id
`tag_type_code` | string | null | The unique code of the selected tag type, `NULL` for text-only tags, or `custom` for custom tag types.
`start_time` | LocalDateTime | Timestamp of the tag (if no duration) or the start time of the tag (with duration).
`end_time` | LocalDateTime | null | Timestamp of the tag's end for events with duration or `NULL` if there is no duration.
`start_day` | string | Day of the tag (if no duration) or the start day of the tag (with duration).
`end_day` | string | null | Day of the tag's end for events with duration or `NULL` if there is no duration.
`comment` | string | null | Additional freeform text on the tag.
`custom_name` | string | null | The name of the tag if the tag_type_code is `custom`.

## ????????? ? `/v2/usercollection/personal_info`
- **??**: ????????????????????????
- **??????**: Single Personal Info Document
- **????????**: `PersonalInfoResponse`
- **??????**:
  - `age` [integer | null]: Age
  - `height` [number | null]: Height
  - `weight` [number | null]: Weight
  - `biological_sex` [string | null]: Biological Sex

### ???????
????? | ? | ????
|-|-|-|
`id` | string | Id
`age` | integer | null | Age
`weight` | number | null | Weight
`height` | number | null | Height
`biological_sex` | string | null | Biological Sex
`email` | string | null | Email

## ????? ? `/v2/usercollection/ring_configuration`
- **??**: ??????????????????????????
- **??????**: Multiple Ring Configuration Documents
- **????????**: `RingConfigurationModel`
- **??????**:
  - `hardware_revision`: (field not found in schema)
  - `color` [RingColor | null]: Color of the ring.
  - `size` [integer | null]: US size of the ring.
  - `serial_number`: (field not found in schema)

### ???????
????? | ? | ????
|-|-|-|
`id` | string | Id
`color` | RingColor | null | Color of the ring.
`design` | RingDesign | null | Design of the ring.
`firmware_version` | string | null | Firmware version of the ring.
`hardware_type` | RingHardwareType | null | Hardware type of the ring.
`set_up_at` | LocalDateTime | null | UTC timestamp indicating when the ring was set up.
`size` | integer | null | US size of the ring.

## ???????? ? `/v2/usercollection/rest_mode_period`
- **??**: ???????????????????????????????????
- **??????**: Multiple Rest Mode Period Documents
- **????????**: `RestModePeriodModel`
- **??????**:
  - `start_datetime`: (field not found in schema)
  - `end_datetime`: (field not found in schema)
  - `reason`: (field not found in schema)

### ???????
????? | ? | ????
|-|-|-|
`id` | string | Id
`end_day` | string | null | End date of rest mode.
`end_time` | LocalDateTime | null | Timestamp when rest mode ended.
`episodes` | array<RestModeEpisode> | Collection of episodes during rest mode, consisting of tags.
`episodes[].tags` | array<string> | Tags selected for the episode.
`episodes[].timestamp` | LocalizedDateTime | Timestamp indicating when the episode occurred.
`start_day` | string | Start date of rest mode.
`start_time` | LocalDateTime | null | Timestamp when rest mode started.
