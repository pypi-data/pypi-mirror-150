"""Import the web-based export back into Python so we can render it in Python."""

import json
import math
import multiprocessing
import jax
import numpy as np
from PIL import Image
import tensorflow as tf
from einops import rearrange
from tqdm import tqdm

def synchronize_jax_hosts():
  """Makes sure that the JAX hosts have all reached this point."""
  # Build an array containing the host_id.
  num_local_devices = jax.local_device_count()
  num_hosts = jax.host_count()
  host_id = jax.host_id()
  dummy_array = np.ones((num_local_devices, 1), dtype=np.int32) * host_id

  # Then broadcast it between all JAX hosts. This makes sure that all hosts are
  # in sync, and have reached this point in the code.
  gathered_array = jax.pmap(
      lambda x: jax.lax.all_gather(x, axis_name='i'), axis_name='i')(
          dummy_array)
  gathered_array = np.reshape(
      gathered_array[0], (num_hosts, num_local_devices, 1))

  # Finally, make sure that the data is exactly what we expect.
  for i in range(num_hosts):
    assert gathered_array[i][0] == i


def parallel_write_images(image_write_fn, img_and_path_list):
  """Parallelizes image writing over JAX hosts and CPU cores.

  Args:
    image_write_fn: A function that takes a tuple as input (path, image) and
      writes the result to disk.
    img_and_path_list: A list of tuples (image, path) containing all the images
      that should be written.
  """
  num_hosts = jax.host_count()
  host_id = jax.host_id()
  num_images = len(img_and_path_list)
  num_images_per_batch = math.ceil(num_images / num_hosts)

  # First shard the images onto each host.
  per_host_images_and_paths = []
  for i in range(num_images_per_batch):
    base_index = i * num_hosts
    global_index = base_index + host_id
    if global_index < num_images:
      per_host_images_and_paths.append(img_and_path_list[global_index])

  # Now within each JAX host, use multi-processing to save the sharded images.
  with multiprocessing.pool.ThreadPool() as pool:
    pool.map(image_write_fn, per_host_images_and_paths)
    pool.close()
    pool.join()

def import_snerg_scene(indir):
  """Imports a scene from web-viewer format"""
  atlas_block_indices = None
  viewdir_mlp_params = {
    'params': {
      'Dense_0': {},
      'Dense_1': {},
      'Dense_3': {},
    }
  }
  render_params = {
    '_grid_size': [None] * 3,
  }
  atlas_params = {}
  scene_params = {
    'min_xyz': [None] * 3,
  }
  input_height = None
  input_width = None
  input_focal = None
  
  with open(indir + '/scene_params.json') as export_scene_params_json:
    export_scene_params = json.load(export_scene_params_json)
    
    render_params['_voxel_size'] = export_scene_params['voxel_size']
    atlas_params['_data_block_size'] = export_scene_params['block_size']
    
    render_params['_grid_size'][0] = export_scene_params['grid_width']
    render_params['_grid_size'][1] = export_scene_params['grid_height']
    render_params['_grid_size'][2] = export_scene_params['grid_depth']
    
    scene_params['min_xyz'][0] = export_scene_params['min_x']
    scene_params['min_xyz'][1] = export_scene_params['min_y']
    scene_params['min_xyz'][2] = export_scene_params['min_z']
    
    atlas_params['atlas_block_size'] = export_scene_params['atlas_width'] // export_scene_params['atlas_blocks_x']

    # input_height = export_scene_params['input_height']
    # input_width = export_scene_params['input_width']
    # input_focal = export_scene_params['input_focal']

    scene_params['worldspace_T_opengl'] = np.array(export_scene_params['worldspace_T_opengl'])
    scene_params['ndc'] = export_scene_params['ndc']
    scene_params['_channels'] = 7

    viewdir_mlp_params['params']['Dense_0']['kernel'] = np.array(export_scene_params['0_weights'])
    viewdir_mlp_params['params']['Dense_1']['kernel'] = np.array(export_scene_params['1_weights'])
    viewdir_mlp_params['params']['Dense_3']['kernel'] = np.array(export_scene_params['2_weights'])
    viewdir_mlp_params['params']['Dense_0']['bias'] = np.array(export_scene_params['0_bias'])
    viewdir_mlp_params['params']['Dense_1']['bias'] = np.array(export_scene_params['1_bias'])
    viewdir_mlp_params['params']['Dense_3']['bias'] = np.array(export_scene_params['2_bias'])

    atlas_width = export_scene_params['atlas_width']
    # export_scene_params['atlas_width'] = atlas.shape[0]
    atlas_height = export_scene_params['atlas_height']
    # export_scene_params['atlas_height'] = atlas.shape[1]
    atlas_depth = export_scene_params['atlas_depth']
    # export_scene_params['atlas_depth'] = atlas.shape[2]
    num_slices = export_scene_params['num_slices']
    # export_scene_params['num_slices'] = len(rgbs)

    atlas_blocks_x = export_scene_params['atlas_blocks_x']
    atlas_blocks_y = export_scene_params['atlas_blocks_y']
    atlas_blocks_z = export_scene_params['atlas_blocks_z']

    # export_scene_params['atlas_blocks_x'] = int(atlas.shape[0] /
    #                                             atlas_params['atlas_block_size'])
    # export_scene_params['atlas_blocks_y'] = int(atlas.shape[1] /
    #                                             atlas_params['atlas_block_size'])
    # export_scene_params['atlas_blocks_z'] = int(atlas.shape[2] /
    #                                             atlas_params['atlas_block_size'])

  # atlas: The SNeRG scene packed as a texture atlas in a [S, S, N, C] numpy
  #   array, where the channels C contain both RGB and features.
  # atlas_block_indices: The indirection grid of the SNeRG scene, represented as
  #   a numpy int32 array of size (bW, bH, bD, 3).

  """ rgbs = []
  alphas = []
  for i in range(0, atlas.shape[2], 4):
    rgb_stack = []
    alpha_stack = []
    for j in range(4):
      plane_index = i + j
      rgb_stack.append(atlas[:, :, plane_index, :][Ellipsis, 0:3].transpose([1, 0, 2]))
      alpha_stack.append(atlas[:, :, plane_index, :][Ellipsis, scene_params['_channels']].transpose([1, 0]))
    rgbs.append(np.concatenate(rgb_stack, axis=0))
    alphas.append(np.concatenate(alpha_stack, axis=0)) """

  # (bW, bH, bD, 3) -> (bD, bH, bW, 3) -> (bD*bH, bW, 3)
  """ atlas_index_image = np.transpose(atlas_block_indices, [2, 1, 0, 3]).reshape(
      (-1, atlas_block_indices.shape[0], 3)).astype(np.uint8) """

  with Image.open(indir + '/atlas_indices.png') as atlas_index_image:
    atlas_index_image = np.array(atlas_index_image)
    # (bD*bH, bW, 3) -> (bW, bH, bD, 3)
    # einops!!
    atlas_block_indices = rearrange(atlas_index_image, '(bD bH) bW idx -> bW bH bD idx', bD = atlas_blocks_z)
    print(atlas_index_image.shape, atlas_block_indices.shape)

  # output_images = []
  # output_paths = []
  # for i, rgb_and_alpha in enumerate(zip(rgbs, alphas)):
  #   rgb, alpha = rgb_and_alpha
  #   rgba = np.concatenate([rgb, np.expand_dims(alpha, -1)], axis=-1)
  #   # uint_multiplier = 2.0**8 - 1.0
  #   # rgba = np.minimum(uint_multiplier,
  #   #                   np.maximum(0.0, np.floor(uint_multiplier * rgba))).astype(
  #   #                       np.uint8)
  #   # output_images.append(rgba)
  #   # atlas_rgba_path = '%s/rgba_%03d.png' % (output_tmp_directory, i)
  #   # output_paths.append(atlas_rgba_path)

  atlas_slice_size = 2048
  atlas = np.empty((atlas_slice_size, atlas_slice_size, 4 * num_slices, 8))
  uint_multiplier = 2.0**8 - 1.0
  for i in tqdm(range(0, 4 * num_slices, 4)):
    with Image.open(indir + f'/rgba_00{i//4}.png') as rgba_slice, Image.open(indir + f'/feature_00{i//4}.png') as feature_slice:
      # convert images to np arrays
      rgba_slice = np.array(rgba_slice)
      # print(rgba_slice.shape)
      feature_slice = np.array(feature_slice)
      # print(feature_slice.shape)

      # divide by uint multiplier
      rgba_slice = rgba_slice / uint_multiplier
      feature_slice = feature_slice / uint_multiplier
  
      [rgb_slice, a_slice] = np.split(rgba_slice, [3], axis=2)

      rgb_planes = np.split(rgb_slice, 4, axis=0)
      a_planes = np.split(a_slice, 4, axis=0)
      feature_planes = np.split(feature_slice, 4, axis=0)

      for j, plane in enumerate(zip(rgb_planes, a_planes, feature_planes)):
        plane_index = i + j
        rgb_plane, a_plane, feature_plane = plane
        # print(rgb_plane.shape, a_plane.shape, feature_plane.shape)
        atlas[:, :, plane_index, 0:3] = rearrange(rgb_plane, 's2 s1 c -> s1 s2 c')
        atlas[:, :, plane_index, 3:-1] = rearrange(feature_plane, 's2 s1 c -> s1 s2 c')
        atlas[:, :, plane_index, -1] = np.squeeze(rearrange(a_plane, 's2 s1 c -> s1 s2 c'))

      # print(rgb_slice.shape)
      # print(a_slice.shape)

      # smash everything into the atlas
      # atlas[:, :, plane_index:plane_index+4, 0:3] = rearrange(rgb_slice, '(s1 stack) s2 c -> s1 s2 stack c', s1=atlas_slice_size)
      # atlas[:, :, plane_index:plane_index+4, 3:-1] = rearrange(feature_slice, '(s1 stack) s2 c -> s1 s2 stack c', s1=atlas_slice_size)
      # atlas[:, :, plane_index:plane_index+4, -1] = rearrange(a_slice, '(s1 stack) s2 1 -> s1 s2
      # stack', s1=atlas_slice_size)

      # atlas[:, :, plane_index:plane_index+4, 0:3] = rearrange(rgb_slice, '(s2 stack) s1 c -> s1 s2 stack c', s2=atlas_slice_size)
      # atlas[:, :, plane_index:plane_index+4, 3:-1] = rearrange(feature_slice, '(s2 stack) s1 c -> s1 s2 stack c', s2=atlas_slice_size)
      # atlas[:, :, plane_index:plane_index+4, -1] = rearrange(a_slice, '(s2 stack) s1 1 -> s1 s2 stack', s2=atlas_slice_size)

  return {
    'atlas': atlas,
    'atlas_block_indices': atlas_block_indices,
    'viewdir_mlp_params': viewdir_mlp_params,
    'render_params': render_params,
    'atlas_params': atlas_params,
    'scene_params': scene_params,
    # input_height,
    # input_width,
    # input_focal,
  }

def compute_scene_size(output_directory, atlas_block_indices, atlas_params,
                       scene_params):
  """Computes the size of an exported SNeRG scene.

  Args:
    output_directory: The root directory where the SNeRG scene was written.
    atlas_block_indices: The indirection grid of the SNeRG scene.
    atlas_params: A dict with params for building the 3D texture atlas.
    scene_params: A dict for scene specific params (bbox, rotation, resolution).

  Returns:
    png_size_gb: The scene size (in GB) when stored as compressed 8-bit PNGs.
    byte_size_gb: The scene size (in GB), stored as uncompressed 8-bit integers.
    float_size_gb: The scene size (in GB), stored as uncompressed 32-bit floats.
  """

  output_png_directory = output_directory + '/png'
  png_files = [
      output_png_directory + '/' + f
      for f in sorted(utils.listdir(output_png_directory))
      if f.endswith('png')
  ]
  png_size_gb = sum(
      [tf.io.gfile.stat(f).length / (1000 * 1000 * 1000) for f in png_files])

  block_index_size_gb = np.array(
      atlas_block_indices.shape).prod() / (1000 * 1000 * 1000)

  active_atlas_blocks = (atlas_block_indices[Ellipsis, 0] >= 0).sum()
  active_atlas_voxels = (
      active_atlas_blocks * atlas_params['atlas_block_size']**3)
  active_atlas_channels = active_atlas_voxels * scene_params['_channels']

  byte_size_gb = active_atlas_channels / (1000 * 1000 *
                                          1000) + block_index_size_gb
  float_size_gb = active_atlas_channels * 4 / (1000 * 1000 *
                                               1000) + block_index_size_gb

  return png_size_gb, byte_size_gb, float_size_gb
