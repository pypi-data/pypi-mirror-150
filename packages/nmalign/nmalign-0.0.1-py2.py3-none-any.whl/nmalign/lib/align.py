from rapidfuzz.process import cdist
from rapidfuzz.string_metric import normalized_levenshtein
import numpy as np

def match(l1, l2, workers=1, cutoff=None):
    """Force alignment of string lists.

    Computes string alignments between each pair among l1 and l2.
    Then iteratively searches the next closest pair. Stores
    the assigned result as injective mapping from l1 to l2.
    (Unmatched or cut off elements will be assigned -1.)
    Returns corresponding list indices and match scores [0,100]
    as a tuple of Numpy arrays.
    """
    assert len(l1) > 0
    assert len(l2) > 0
    assert isinstance(l1[0], str)
    assert isinstance(l2[0], str)
    dist = cdist(l1, l2, scorer=normalized_levenshtein, score_cutoff=cutoff, workers=workers)
    ind1, ind2 = np.unravel_index(np.argmin(dist), dist.shape)
    dim1 = len(l1)
    dim2 = len(l2)
    idx1 = np.arange(dim1)
    idx2 = np.arange(dim2)
    keep1 = np.ones(dim1, dtype=np.bool)
    keep2 = np.ones(dim2, dtype=np.bool)
    result = -1 * np.ones(dim1, dtype=np.int)
    scores = np.zeros(dim1, dtype=dist.dtype)
    for _ in range(dim1):
        distview = dist[np.ix_(keep1,keep2)]
        if not distview.size:
            break
        ind1, ind2 = np.unravel_index(np.argmax(distview, axis=None), distview.shape)
        score = distview[ind1,ind2]
        if isinstance(cutoff, (int, float)) and score < cutoff:
            break
        ind1 = idx1[keep1][ind1]
        ind2 = idx2[keep2][ind2]
        assert result[ind1] < 0
        assert keep1[ind1]
        assert keep2[ind2]
        result[ind1] = ind2
        scores[ind1] = score
        keep1[ind1] = False
        keep2[ind2] = False
    return result, scores
