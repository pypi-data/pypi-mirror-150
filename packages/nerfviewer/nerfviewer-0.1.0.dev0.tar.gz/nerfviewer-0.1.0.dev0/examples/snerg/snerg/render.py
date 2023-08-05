from snerg.snerg_import import import_snerg_scene
from snerg.rendering import atlas_raymarch_image_tf, post_process_render
from snerg.nerf import model_utils

def create_scene(indir):
  imported_scene = import_snerg_scene(indir)
  imported_scene['scene_params']['_use_pixel_centers'] = True
  imported_scene['scene_params']['near'] = 0.33
  imported_scene['scene_params']['far'] = 6.0

  # TODO: look at blender.yaml for more settings if needed
  viewdir_mlp = model_utils.MLP(
    net_width=512,
  )

  def render(h, w, focal, camtoworld):
    rgb, alpha = atlas_raymarch_image_tf(h, w, focal, camtoworld,
      imported_scene['atlas'],
      imported_scene['atlas_block_indices'],
      imported_scene['atlas_params'],
      imported_scene['scene_params'],
      imported_scene['render_params'])

    return post_process_render(
      viewdir_mlp, imported_scene['viewdir_mlp_params'], rgb, alpha, h, w,
                        focal, camtoworld, imported_scene['scene_params'])
  
  return render

import tensorflow as tf
import numpy as np

trans_t = lambda t : tf.convert_to_tensor([
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,t],
    [0,0,0,1],
], dtype=tf.float32)

rot_phi = lambda phi : tf.convert_to_tensor([
    [1,0,0,0],
    [0,tf.cos(phi),-tf.sin(phi),0],
    [0,tf.sin(phi), tf.cos(phi),0],
    [0,0,0,1],
], dtype=tf.float32)

rot_theta = lambda th : tf.convert_to_tensor([
    [tf.cos(th),0,-tf.sin(th),0],
    [0,1,0,0],
    [tf.sin(th),0, tf.cos(th),0],
    [0,0,0,1],
], dtype=tf.float32)


def pose_spherical(theta, phi, radius):
    c2w = trans_t(radius)
    c2w = rot_phi(phi/180.*np.pi) @ c2w
    c2w = rot_theta(theta/180.*np.pi) @ c2w
    c2w = np.array([[-1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]]) @ c2w
    return c2w

example_pose = pose_spherical(100, -30, 4)
