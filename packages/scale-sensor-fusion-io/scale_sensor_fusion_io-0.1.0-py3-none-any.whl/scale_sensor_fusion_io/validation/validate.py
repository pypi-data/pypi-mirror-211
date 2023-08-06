from dataclasses import asdict, dataclass
from typing import List

import numpy as np
from scale_sensor_fusion_io.models import (
    CameraDistortion,
    CameraIntrinsics,
    CameraSensor,
    LidarSensor,
    LidarSensorFrame,
    LidarSensorPoints,
    PosePath,
    RadarSensor,
    RadarSensorFrame,
    RadarSensorPoints,
    Scene,
    Sensor,
    SensorKind,
)

from .error import (
    DataValidationError,
    ErrorDetails,
    PathField,
    ValidationResult,
)
from .helpers import is_monotonically_increasing

MICRO_IN_SEC = 1e6


def _handle_result(
    res: ValidationResult, error_details: List[ErrorDetails], path: List[PathField] = []
) -> None:
    if res:
        error_details.extend(
            res.details if not path else res.prepend_path(path).details
        )

    return None


def validate_radar(sensor: RadarSensor) -> ValidationResult:
    """Validate lidar sensor"""
    error_details: List[ErrorDetails] = []
    content_timestamps = [frame.timestamp for frame in sensor.frames]

    _handle_result(
        validate_timestamps(content_timestamps), error_details, path=["frames"]
    )
    _handle_result(validate_fps(content_timestamps), error_details)

    if len(error_details) > 0:
        return DataValidationError(details=error_details)

    return None


def validate_timestamps(timestamps: List[int]) -> ValidationResult:
    error_details: List[ErrorDetails] = []
    if any(ts < 0 for ts in timestamps):
        error_details.append(
            ErrorDetails.from_msg(
                "timestamps must not be negative",
            )
        )
    if not is_monotonically_increasing(timestamps):
        error_details.append(
            ErrorDetails.from_msg(
                "timestamps be monotonically increasing",
            )
        )
    if len(error_details) > 0:
        return DataValidationError(details=error_details)
    return None


def validate_fps(timestamps: List[int], max_fps: int = 100) -> ValidationResult:
    error_details: List[ErrorDetails] = []

    # compute approximate fps from timestamps
    avg_ts_diffs = np.mean([t2 - t1 for t1, t2 in zip(timestamps, timestamps[1:])])
    fps = MICRO_IN_SEC / avg_ts_diffs

    if fps > max_fps:
        error_details.append(
            ErrorDetails.from_msg(
                f"approximate fps is too high: {fps} > {max_fps}",
            )
        )

    if len(error_details) > 0:
        return DataValidationError(details=error_details)

    return None


def validate_lidar(sensor: LidarSensor) -> ValidationResult:
    """Validate lidar sensor"""
    error_details: List[ErrorDetails] = []
    content_timestamps = [frame.timestamp for frame in sensor.frames]

    _handle_result(
        validate_timestamps(content_timestamps), error_details, path=["frames"]
    )
    _handle_result(validate_fps(content_timestamps), error_details)

    for frame in sensor.frames:
        ### validate all fields of points have same length
        pos_length = len(frame.points.positions)
        if (
            frame.points.intensities is not None
            and len(frame.points.intensities) != pos_length
        ):
            error_details.append(
                ErrorDetails.from_msg(
                    f"length of positions ({len(frame.points.positions)}) and intensities ({len(frame.points.intensities)}) must be the same"
                )
            )

        if frame.points.colors is not None and len(frame.points.colors) != pos_length:
            error_details.append(
                ErrorDetails.from_msg(
                    f"length of positions ({len(frame.points.positions)}) and colors ({len(frame.points.colors)}) must be the same"
                )
            )

        if (
            frame.points.timestamps is not None
            and len(frame.points.timestamps) != pos_length
        ):
            error_details.append(
                ErrorDetails.from_msg(
                    f"length of positions ({len(frame.points.positions)}) and timestamps ({len(frame.points.timestamps)}) must be the same"
                )
            )

    if len(error_details) > 0:
        return DataValidationError(details=error_details)

    return None


def validate_camera(sensor: CameraSensor) -> ValidationResult:
    """Validate camera sensor"""
    error_details: List[ErrorDetails] = []

    # camera content
    content_timestamps: List[int] = []
    content_timestamps_path: List[PathField] = []
    if sensor.video:
        content_timestamps = sensor.video.timestamps
        content_timestamps_path = ["video"]
    elif sensor.images:
        content_timestamps = [img.timestamp for img in sensor.images]
        content_timestamps_path = ["images"]
    else:
        error_details.append(
            ErrorDetails.from_msg('Exactly one of "images" or "video" expected')
        )

    _handle_result(
        validate_timestamps(content_timestamps),
        error_details,
        path=content_timestamps_path,
    )
    _handle_result(
        validate_fps(content_timestamps),
        error_details,
    )

    if len(error_details) > 0:
        return DataValidationError(details=error_details)

    return None


def validate_sensor(sensor: Sensor) -> ValidationResult:
    error_details: List[ErrorDetails] = []
    if sensor.type is SensorKind.Camera:
        _handle_result(validate_camera(sensor), error_details)
    elif sensor.type is SensorKind.Lidar:
        _handle_result(validate_lidar(sensor), error_details)
    elif sensor.type is SensorKind.Radar:
        _handle_result(validate_radar(sensor), error_details)
    else:
        error_details.append(
            ErrorDetails(
                path=["type"], errors=[f"Invalid sensor type provided: {sensor.type}"]
            )
        )
    if len(error_details) > 0:
        return DataValidationError(details=error_details)

    return None


def validate_scene(scene: Scene) -> ValidationResult:
    """Validate scene"""
    error_details: List[ErrorDetails] = []
    if scene.sensors:
        for sensor in scene.sensors:
            _handle_result(
                validate_sensor(sensor),
                error_details,
                path=["sensors", str(sensor.id)],
            )

        if len(scene.sensors) != len(set([sensor.id for sensor in scene.sensors])):
            error_details.append(
                ErrorDetails.from_msg("Sensor ids must be unique", path=["sensors"])
            )

    if scene.time_unit != "microseconds":
        error_details.append(
            ErrorDetails.from_msg(
                f"Invalid time unit provided: {scene.time_unit}. Expected: microseconds"
            )
        )

    if scene.time_offset is not None and scene.time_offset < 0:
        error_details.append(
            ErrorDetails.from_msg("Scene timestamp must not be negative")
        )

    if len(error_details) > 0:
        return DataValidationError(details=error_details)
    return None
