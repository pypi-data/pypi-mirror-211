import matplotlib.colors as mcolors

""" Metropolis-Hastings"""
prob_recomb = [0.0, 0.06, 0.09, 0.18, 0.17, 0.17, 0.18, 0.09, 0.06, 0.0] # link between each bead breaking and recombining
# prob_num_of_recomb = [0.36, 0.301, 0.146, 0.193] # just 1 recombination for now
""" Trait """
trait_natural_marker_weights = [0.,0.1,0.1,0.,0.2,
                                0.,0.2,0.2,0.1,0.1]

trait_alpha_marker_weights = [1.4,0.3,0.1,0.,0.,
                              0.,0.,1.,1.7,1.1]
num_of_markers = len(trait_natural_marker_weights)

# color mapping
base_alpha = [0.3,0.5,.9]
base_alpha_str = [str(int(x*100)) for x in base_alpha]
bmap  = {
    0: "#FFBF00"+base_alpha_str[0],
    1: "#FF7F50"+base_alpha_str[1],
    2: "#003566"+base_alpha_str[2] # or -1 (het)
}


def get_bmap():
    global bmap
    return bmap

def hex2rgba(hexcode="",alpha=1.):
  # Convert hexcode to RGBA tuple
  rgba = mcolors.to_rgba(hexcode, alpha=alpha)
  # return tuple(int(c * 255) for c in rgba) # 255 range
  return [int(c * 255) for c in rgba]

def get_bmap_rgba():
    global bmap
    bmap_rgba = {}
    for k, a in zip(bmap.keys(), base_alpha):
        bmap_rgba[k] = hex2rgba(bmap[k], alpha=a)
    return bmap_rgba

def get_num_of_markers():
    global num_of_markers
    return num_of_markers

def get_prob_recomb():
    global prob_recomb
    return prob_recomb

def get_trait_natural_marker_weights():
    global trait_natural_marker_weights
    return trait_natural_marker_weights

def get_trait_alpha_marker_weights():
    global trait_alpha_marker_weights
    return trait_alpha_marker_weights