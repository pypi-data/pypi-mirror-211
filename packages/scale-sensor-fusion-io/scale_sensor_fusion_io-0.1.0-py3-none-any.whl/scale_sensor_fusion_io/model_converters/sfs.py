from dataclasses import asdict
from typing import List, Optional

import numpy as np
from scale_sensor_fusion_io.models import (
    CameraSensor,
    CameraDistortion,
    CameraIntrinsics,
    CameraSensorImage,
    CameraSensorVideo,
    LidarSensor,
    LidarSensorFrame,
    LidarSensorPoints,
    RadarSensor,
    RadarSensorFrame,
    RadarSensorPoints,
    Scene,
    PosePath,
)
from scale_sensor_fusion_io.spec import SFS


def from_lidarpoints_sfs(points: SFS.LidarSensorPoints) -> LidarSensorPoints:
    return LidarSensorPoints(
        positions=points.positions.reshape(-1, 3),
        colors=points.colors.reshape(-1, 3) if points.colors is not None else None,
        intensities=points.intensities,
        timestamps=points.timestamps if points.timestamps is not None else None,
    )


def to_lidarpoints_sfs(points: LidarSensorPoints) -> SFS.LidarSensorPoints:
    return SFS.LidarSensorPoints(
        positions=points.positions.reshape(-1, 3),
        colors=points.colors.reshape(-1, 3) if points.colors is not None else None,
        intensities=points.intensities,
        timestamps=points.timestamps,
    )


def from_radarpoints_sfs(points: SFS.RadarSensorPoints) -> RadarSensorPoints:
    return RadarSensorPoints(
        positions=points.positions.reshape(-1, 3),
        directions=points.directions.reshape(-1, 3)
        if points.directions is not None
        else None,
        timestamps=points.timestamps if points.timestamps is not None else None,
    )


def to_radarpoints_sfs(points: RadarSensorPoints) -> SFS.RadarSensorPoints:
    return SFS.RadarSensorPoints(
        positions=points.positions.reshape(-1, 3),
        directions=points.directions.reshape(-1, 3)
        if points.directions is not None
        else None,
        timestamps=points.timestamps,
    )


def from_pose_sfs(posePath: SFS.PosePath) -> PosePath:
    timestamps = np.array(t for t in posePath.timestamps)
    values = np.vstack([v for v in posePath.values])

    return PosePath(data=values, index=timestamps)


def to_pose_sfs(poses: PosePath) -> SFS.PosePath:
    return SFS.PosePath(
        timestamps=poses.index.tolist(),
        values=poses.values.tolist(),
    )


def from_camera_timestamp(camera_sensor: SFS.CameraSensor) -> List[int]:
    if camera_sensor.images:
        return [i.timestamp for i in camera_sensor.images]
    elif camera_sensor.video:
        return camera_sensor.video.timestamps
    else:
        raise Exception("Camera sensor has no timestamp info")


def from_intrinsics_sfs(intrinsics: SFS.CameraIntrinsics) -> CameraIntrinsics:
    return CameraIntrinsics(
        fx=intrinsics.fx,
        fy=intrinsics.fy,
        cx=intrinsics.cx,
        cy=intrinsics.cy,
        width=intrinsics.width,
        height=intrinsics.height,
        distortion=from_distortion_sfs(intrinsics.distortion),
    )


"""
NOTE: The distortion conversion does not need to keep track of the order of the
coefficients since this is managed by the dataclass themselves. However this implies
that 1) distortion parameters must remain dataclasses and 2) the ordering of the
variables matters.
"""


def from_distortion_sfs(
    distortion: Optional[SFS.CameraDistortion],
) -> Optional[CameraDistortion]:
    if distortion is None or not distortion.model:
        return None

    return CameraDistortion.from_values(
        model=distortion.model, values=distortion.params
    )


def to_intrinsics_sfs(intrinsics: CameraIntrinsics) -> SFS.CameraIntrinsics:
    return SFS.CameraIntrinsics(
        fx=intrinsics.fx,
        fy=intrinsics.fy,
        cx=intrinsics.cx,
        cy=intrinsics.cy,
        width=intrinsics.width,
        height=intrinsics.height,
        distortion=to_distortion_sfs(intrinsics.distortion),
    )


def to_distortion_sfs(
    distortion: Optional[CameraDistortion],
) -> Optional[SFS.CameraDistortion]:
    if not distortion or not distortion.model:
        return None

    params = [v for k, v in asdict(distortion.params).items() if k != "model"]
    return SFS.CameraDistortion(model=distortion.model.value, params=params)


def from_scene_spec_sfs(scene: SFS.Scene) -> Scene:
    new_scene = Scene(sensors=[])
    if not scene.sensors:
        return new_scene

    if not new_scene.sensors:
        new_scene.sensors = []
    for sensor in scene.sensors:
        if type(sensor) is SFS.LidarSensor:
            lidar_sensor = sensor
            poses = from_pose_sfs(lidar_sensor.poses)
            frames = [
                LidarSensorFrame(
                    timestamp=int(f.timestamp), points=from_lidarpoints_sfs(f.points)
                )
                for f in lidar_sensor.frames
            ]
            l_sensor = LidarSensor(id=lidar_sensor.id, poses=poses, frames=frames)
            new_scene.sensors.append(l_sensor)

        elif type(sensor) is SFS.RadarSensor:
            radar_sensor = sensor
            r_poses = from_pose_sfs(radar_sensor.poses)

            r_frames = [
                RadarSensorFrame(
                    timestamp=int(f.timestamp), points=from_radarpoints_sfs(f.points)
                )
                for f in radar_sensor.frames
            ]
            r_sensor = RadarSensor(id=radar_sensor.id, poses=r_poses, frames=r_frames)
            new_scene.sensors.append(r_sensor)

        elif type(sensor) is SFS.CameraSensor:
            camera_sensor = sensor
            c_poses = from_pose_sfs(camera_sensor.poses)
            intrinsics = from_intrinsics_sfs(camera_sensor.intrinsics)
            video, images = None, None

            # sfio and SFS video/images are exactly the same but separated
            # for spec purposes
            if camera_sensor.video:
                video = CameraSensorVideo(**asdict(camera_sensor.video))

            if camera_sensor.images:
                images = [CameraSensorImage(**asdict(i)) for i in camera_sensor.images]

            new_scene.sensors.append(
                CameraSensor(
                    id=camera_sensor.id,
                    poses=c_poses,
                    intrinsics=intrinsics,
                    video=video,
                    images=images,
                )
            )
    return new_scene


def to_scene_spec_sfs(scene: Scene) -> SFS.Scene:
    sensors: List[SFS.Sensor] = []
    if scene.sensors is None:
        return SFS.Scene()

    for sensor in scene.sensors:
        if isinstance(sensor, SFS.CameraSensor):
            video, images = None, None

            if sensor.video:
                video = SFS.CameraSensorVideo(**asdict(sensor.video))

            if sensor.images:
                images = [SFS.CameraSensorImage(**asdict(i)) for i in sensor.images]

            sensors.append(
                SFS.CameraSensor(
                    id=sensor.id,
                    poses=to_pose_sfs(sensor.poses),
                    intrinsics=to_intrinsics_sfs(sensor.intrinsics),
                    video=video,
                    images=images,
                )
            )

        if isinstance(sensor, SFS.RadarSensor):
            sensors.append(
                SFS.RadarSensor(
                    id=sensor.id,
                    poses=to_pose_sfs(sensor.poses),
                    frames=[
                        SFS.RadarSensorFrame(
                            timestamp=frame.timestamp,
                            points=to_radarpoints_sfs(frame.points),
                        )
                        for frame in sensor.frames
                    ],
                )
            )

        if isinstance(sensor, SFS.LidarSensor):
            sensors.append(
                SFS.LidarSensor(
                    id=sensor.id,
                    poses=to_pose_sfs(sensor.poses),
                    frames=[
                        SFS.LidarSensorFrame(
                            timestamp=frame.timestamp,
                            points=to_lidarpoints_sfs(frame.points),
                        )
                        for frame in sensor.frames
                    ],
                )
            )

    return SFS.Scene(
        sensors=sensors, time_offset=scene.time_offset, time_unit=scene.time_unit
    )
