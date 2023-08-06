import numpy as np
from astropy.visualization import PercentileInterval
import napari.viewer


def get_display_range(arr, percentile=99):
    p = PercentileInterval(percentile)
    p_limits = {
        c: p.get_limits(arr.sel(channel=c).data.ravel().clip(0, 1000000))
        for c in arr.channel.values
    }
    p1 = np.array([*[p[0] for p in p_limits.values()]])[..., None, None]
    p2 = np.array([*[p[1] for p in p_limits.values()]])[..., None, None]
    return p1, p2


def create_animation(output, start=1, end=100):
    from napari_animation import Animation

    try:
        viewer = globals()['viewer']
    except KeyError:
        viewer = napari.viewer.current_viewer()

    animation = Animation(viewer)
    _, *size = viewer.dims.current_step
    for i in range(start, end):
        print(f"Capturing step {i}")
        viewer.dims.update({'current_step': (i-1, *size)})
        animation.capture_keyframe()

    print(f"Writing output to {output}")
    animation.animate(output)
