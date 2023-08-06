import random
import numpy as np
from .config import get_num_of_markers, get_prob_recomb, get_trait_natural_marker_weights, \
    get_trait_alpha_marker_weights, get_bmap_rgba
from .trait import _line2traited_value

num_of_markers = get_num_of_markers()
prob_recomb = get_prob_recomb()
trait_natural_marker_weights = get_trait_natural_marker_weights()
trait_alpha_marker_weights = get_trait_alpha_marker_weights()
bmap_rgba = get_bmap_rgba()


def reset():
    global num_of_markers, prob_recomb, trait_natural_marker_weights, trait_alpha_marker_weights, bmap_rgba
    num_of_markers = get_num_of_markers()
    prob_recomb = get_prob_recomb()
    trait_natural_marker_weights = get_trait_natural_marker_weights()
    trait_alpha_marker_weights = get_trait_alpha_marker_weights()
    bmap_rgba = get_bmap_rgba()


def line2traited_value(lines):
    return _line2traited_value(lines, bmap_rgba, trait_alpha_marker_weights, trait_natural_marker_weights)


def get_proposed_array(lineA, lineB, indices):
    """

    :param lineA:
    :param lineB:
    :param indices:
    :return:
    """
    assert ((len(lineA) == len(indices)) and (len(lineB) == len(lineA)))
    break_index = None
    for i in range(len(lineA)):
        if random.random() <= indices[i]:
            break_index = i
            break
    if break_index is not None:
        return lineA[:break_index] + lineB[break_index:]
    return lineA


def metropolis_hastings(lineA, lineB, indices, num_samples):
    """

    :param lineA:
    :param lineB:
    :param indices:
    :param num_samples:
    :return:
    """
    current_array = np.array(lineA)
    samples = [current_array]
    current_sum = np.sum(current_array)
    for _ in range(num_samples):
        proposed_array = get_proposed_array(lineA, lineB, indices)
        proposed_sum = np.sum(proposed_array)
        if current_sum == 0:
            acceptance_prob = 1
        else:
            acceptance_prob = min(1, proposed_sum / current_sum)
        if random.random() <= acceptance_prob:
            current_array = np.array(proposed_array)
            current_sum = proposed_sum
        samples.append(current_array)
    return samples


def get_mask(num_samples=10000):
    """

    :param num_samples:
    :return:
    """
    lineA = [0] * num_of_markers
    lineB = [1] * num_of_markers
    return np.array(metropolis_hastings(lineA, lineB, prob_recomb, num_samples))


def mask2progeny(lineA, lineB, mask):
    """

    :param lineA:
    :param lineB:
    :param mask:
    :return:
    """
    return np.where(mask == 0, lineA, lineB)


def make_dataset(dataset_num=10000):
    """

    :param dataset_num:
    :return:
    """
    """ lines """
    data = np.random.choice([0, 1, 2], size=(dataset_num, 10), p=[0.2, 0.5, 0.3])
    progeny_num = 5
    mask = get_mask(num_samples=progeny_num)
    mask = np.unique(mask, axis=0)

    def choose_nIDX(n=2):
        return np.random.choice(dataset_num, size=n, replace=False)

        # Recombination and shuffle (mimic a pedigree tree with some recombination)

    iter = 5000
    for _ in range(iter):
        ids = choose_nIDX(n=2)

        mask = get_mask(num_samples=progeny_num)
        mask = np.unique(mask, axis=0)
        _idx = choose_nIDX(n=len(mask))
        _data = mask2progeny(data[ids[0]], data[ids[1]], mask)
        data[_idx] = _data
    return data
