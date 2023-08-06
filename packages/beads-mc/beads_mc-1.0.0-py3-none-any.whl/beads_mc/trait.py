import numpy as np


def blend_rgba(rgba_list, weights):
    blended_rgba = np.sum(np.minimum(rgba_list, 255) * weights[:, np.newaxis], axis=0)
    return tuple(blended_rgba.astype(int))


def mappedLine2traitValue(traited_lines, alpha_weights=None, trait_weights=None):
    assert len(alpha_weights) == len(trait_weights)
    assert len(alpha_weights) == traited_lines.shape[1]
    traited_lines[:, :, 3] *= alpha_weights
    trait_values = [blend_rgba(rgba_list=tline.astype(int), weights=trait_weights) for tline in traited_lines]
    return trait_values


def _line2traited_value(lines: np.array,
                       bmap_rgba: dict,
                       trait_alpha_marker_weights:list,
                       trait_natural_marker_weights:list):
    """ line = [1,0,-1] +trait (alpha) --> blended_trait
      combine(lrgba,natural_weights,trait_weights) --> trait_value
      NEEDS alpha_weights

  """
    # 1. lines [0,1,1] --> [(255, 127, 80, 255), (255, 191, 0, 255), (223, 255, 0, 255)]
    mapped_rgba = np.array([bmap_rgba[x] for x in lines.flatten()]).reshape(lines.shape[0], lines.shape[1], -1).astype(
        float)
    # 2. add alpha: Trait adding effect on each marker (alpha of the rgba is reduced according to alpha_weights)
    traited_values = mappedLine2traitValue(mapped_rgba,
                                           alpha_weights=np.array(trait_alpha_marker_weights),
                                           trait_weights=np.array(trait_natural_marker_weights))
    return traited_values
