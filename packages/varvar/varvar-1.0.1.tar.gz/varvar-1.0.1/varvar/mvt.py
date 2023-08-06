import numpy as np
import numba
from numba.pycc import CC

cc = CC("_mvt")

@cc.export("single_best_multiplicative", "UniTuple(float64, 2)(float64[::1], float64[::1])")
def single_best_multiplicative(y2_over_s2, log_s2) -> ("log-likelihood", "s2"):
    m = np.mean(y2_over_s2)
    return -len(y2_over_s2)/2 * (np.log(m) - 1 + np.log(2 * np.pi)) - np.sum(log_s2)/2, m

@cc.export(
    "hist_best_split",
    "Tuple((float64, float64, float64, float64, float64, unicode_type))(float64[::1], uint8[::1], float64[::1], float64[::1])"
)
def hist_best_split(bins, inds, y2_over_s2, log_s2) -> ("log-likelihood1", "s2_1", "log-likelihood2", "s2_2", "threshold", "deault direction"):
    DEFAULT_DIRECTION_IF_NO_NANS = "left"
    
    counts = np.zeros(len(bins), np.uint32)
    y_s_sums = np.zeros(len(bins), np.float32)
    log_sums = np.zeros(len(bins), np.float32)

    # for i, ys, lg in zip(inds, y2_over_s2, log_s2):
    #     counts[i] += 1
    #     y_s_sums[i] += ys
    #     log_sums[i] += lg
    
    n_node_samples = len(inds)
    unrolled_upper = (n_node_samples // 4) * 4
    
    for i in range(0, unrolled_upper, 4):
        ind0 = inds[i]
        ind1 = inds[i+1]
        ind2 = inds[i+2]
        ind3 = inds[i+3]
        
        y_s_sums[ind0] += y2_over_s2[i]
        y_s_sums[ind1] += y2_over_s2[i+1]
        y_s_sums[ind2] += y2_over_s2[i+2]
        y_s_sums[ind3] += y2_over_s2[i+3]
        
        log_sums[ind0] += log_s2[i]
        log_sums[ind1] += log_s2[i+1]
        log_sums[ind2] += log_s2[i+2]
        log_sums[ind3] += log_s2[i+3]
        
        counts[ind0] += 1
        counts[ind1] += 1
        counts[ind2] += 1
        counts[ind3] += 1
    
    for i in range(unrolled_upper, n_node_samples):
        ind0 = inds[i]
        y_s_sums[ind0] += y2_over_s2[i]
        log_sums[ind0] += log_s2[i]
        counts[ind0] += 1
        
    first_nonzero = np.argmax(np.hstack((counts[:-1], np.ones(1, counts.dtype))) != 0)
    last_nonzero = len(counts) - 1 - np.argmax(np.hstack((counts[:-1][::-1], np.ones(1, counts.dtype))) != 0)
    if first_nonzero >= last_nonzero - 1:
        return (np.NINF, np.nan, np.NINF, np.nan, np.nan, DEFAULT_DIRECTION_IF_NO_NANS)
    
    bins = np.hstack((bins[first_nonzero:last_nonzero], bins[-1:]))
    counts = np.hstack((counts[first_nonzero:last_nonzero], counts[-1:]))
    y_s_sums = np.hstack((y_s_sums[first_nonzero:last_nonzero], y_s_sums[-1:]))
    log_sums = np.hstack((log_sums[first_nonzero:last_nonzero], log_sums[-1:]))

    right_forwards_counts = np.cumsum(counts[:-2])
    right_forwards_y_s_sums = np.cumsum(y_s_sums[:-2])
    right_forwards_log_sums = np.cumsum(log_sums[:-2])
    right_forwards_ll = -(right_forwards_counts/2) * (np.log(right_forwards_y_s_sums / right_forwards_counts) - 1 + np.log(2 * np.pi)) - right_forwards_log_sums/2

    left_backwards_counts = np.cumsum(counts[1:-1][::-1])[::-1]
    left_backwards_y_s_sums = np.cumsum(y_s_sums[1:-1][::-1])[::-1]
    left_backwards_log_sums = np.cumsum(log_sums[1:-1][::-1])[::-1]
    left_backwards_ll = -(left_backwards_counts/2) * (np.log(left_backwards_y_s_sums / left_backwards_counts) - 1 + np.log(2 * np.pi)) - left_backwards_log_sums/2

    if counts[-1] == 0:
        i = np.argmax(right_forwards_ll + left_backwards_ll)

        forwards_counts = right_forwards_counts
        forwards_y_s_sums = right_forwards_y_s_sums
        forwards_ll = right_forwards_ll

        backwards_counts = left_backwards_counts
        backwards_y_s_sums = left_backwards_y_s_sums
        backwards_ll = left_backwards_ll

        direction = DEFAULT_DIRECTION_IF_NO_NANS
    else:
        left_forwards_counts = right_forwards_counts + counts[-1]
        left_forwards_y_s_sums = right_forwards_y_s_sums + y_s_sums[-1]
        left_forwards_log_sums = right_forwards_log_sums + log_sums[-1]
        left_forwards_ll = -(left_forwards_counts/2) * (np.log(left_forwards_y_s_sums / left_forwards_counts) - 1 + np.log(2 * np.pi)) - left_forwards_log_sums/2

        right_backwards_counts = left_backwards_counts + counts[-1]
        right_backwards_y_s_sums = left_backwards_y_s_sums + y_s_sums[-1]
        right_backwards_log_sums = left_backwards_log_sums + log_sums[-1]
        right_backwards_ll = -(right_backwards_counts/2) * (np.log(right_backwards_y_s_sums / right_backwards_counts) - 1 + np.log(2 * np.pi)) - right_backwards_log_sums/2

        left_ll = left_forwards_ll + left_backwards_ll
        right_ll = right_forwards_ll + right_backwards_ll

        if np.max(left_ll) > np.max(right_ll):
            i = np.argmax(left_ll)

            forwards_counts = left_forwards_counts
            forwards_y_s_sums = left_forwards_y_s_sums
            forwards_ll = left_forwards_ll

            backwards_counts = left_backwards_counts
            backwards_y_s_sums = left_backwards_y_s_sums
            backwards_ll = left_backwards_ll

            direction = "left"
        else:
            i = np.argmax(right_ll)

            forwards_counts = right_forwards_counts
            forwards_y_s_sums = right_forwards_y_s_sums
            forwards_ll = right_forwards_ll

            backwards_counts = right_backwards_counts
            backwards_y_s_sums = right_backwards_y_s_sums
            backwards_ll = right_backwards_ll

            direction = "right"

    ll1 = forwards_ll[i]
    s2_1 = forwards_y_s_sums[i] / forwards_counts[i]
    ll2 = backwards_ll[i]
    s2_2 = backwards_y_s_sums[i] / backwards_counts[i]

    return ll1, s2_1, ll2, s2_2, bins[i], direction

l = numba.typed.List()
l.append(np.array([1.]))
list_of_arrays_type = numba.typeof(l)

l = numba.typed.List()
l.append(np.array([1], np.uint8))
list_of_ints_type = numba.typeof(l)

@cc.export(
    "best_split",
    numba.types.Tuple((numba.types.float64, numba.types.float64, numba.types.float64, numba.types.float64, numba.types.float64, numba.types.unicode_type, numba.types.int64))(
        list_of_ints_type, list_of_arrays_type, numba.types.float64[::1], numba.types.float64[::1], numba.types.boolean
    )
)
def best_split(X_inds, X_midpoints, y2_over_s2, log_s2, threads=False) -> ("log-likelihood1", "s2_1", "log-likelihood2", "s2_2", "threshold", "deault direction", "feature index"):
    splits = [(np.NINF, np.nan, np.NINF, np.nan, np.nan, "left")] * len(X_inds)
    
    for i in range(len(X_inds)):
        splits[i] = hist_best_split(X_midpoints[i], X_inds[i], y2_over_s2, log_s2)

    best_i = 0
    best = splits[0][0] + splits[0][2]
    for i in range(1, len(splits)):
        if splits[i][0] + splits[i][2] > best:
            best_i = i
            best = splits[i][0] + splits[i][2]
    return splits[best_i] + (best_i,)
    
tree_instance = numba.typed.List([(1., 2., 'left', -1)])
trees_instance = numba.typed.List([tree_instance])
tree_type = numba.typeof(tree_instance)
trees_type = numba.typeof(trees_instance)

@cc.export(
    "best_tree",
    tree_type(list_of_ints_type, list_of_arrays_type, numba.types.float64[::1], numba.types.float64[::1], numba.types.int64, numba.types.float64, numba.types.float64, numba.types.int64, numba.types.boolean)
)
def best_tree(
    X_inds, X_midpoints, y2_over_s2, log_s2, max_depth, mingain, ll_pred=np.NINF, min_split_size=1000, threads=True
) -> 'List[Union[Tuple["right tree offset", "threshold", "deault direction", "feature index"), Tuple["log-likelihood", "s2", '', '')]]':
    if max_depth <= 0:
        return numba.typed.List([single_best_multiplicative(y2_over_s2, log_s2) + ('', -1)])
    
    ll1, s2_1, ll2, s2_2, threshold, default, feature = best_split(X_inds, X_midpoints, y2_over_s2, log_s2, threads=threads)
     
    if ll1 + ll2 > ll_pred + mingain:
        lls = [ll1, ll2]
        x_inds = X_inds[feature]
        x_midpoints = X_midpoints[feature]
        nans = x_inds == len(x_midpoints) - 1
        threshold_ind = np.argmax(x_midpoints >= threshold)
        
        if default == "left":
            inds0 = [
                np.less_equal(x_inds, threshold_ind) | nans,
                np.greater(x_inds, threshold_ind)
            ]
        else:
            inds0 = [
                np.less_equal(x_inds, threshold_ind),
                np.greater(x_inds, threshold_ind) | nans
            ]
        
        tree_instance = numba.typed.List()
        tree_instance.append((1., 2., 'left', -1))
        left_right = [tree_instance, tree_instance]
        
        ss = np.sum(inds0[0])
        
        if ss >= min_split_size and len(log_s2) - ss >= min_split_size:
            for i in range(2):
                inds = inds0[i]
                ll = lls[i]
                left_right[i] = (
                    best_tree(
                        numba.typed.List([x[inds] for x in X_inds]),
                        X_midpoints,
                        y2_over_s2[inds], log_s2[inds],
                        max_depth - 1, mingain,
                        ll,
                        min_split_size=min_split_size,
                        threads=threads
                    )
                )

            r = numba.typed.List([(len(left_right[0]) + 0., threshold, default, feature)])
            r.extend(left_right[0])
            r.extend(left_right[1])

            return r
    
    return numba.typed.List([single_best_multiplicative(y2_over_s2, log_s2) + ('', -1)])

@cc.export(
    "predict_tree_inplace",
    numba.types.void(tree_type, numba.types.int64, list_of_arrays_type, numba.types.float64[::1], numba.types.int64[::1])
)
def predict_tree_inplace(tree, offset, X, y, inds):
    if not X:
        return
    if tree[offset][3] == -1:
        y[inds] *= tree[offset][1]
    else:
        right_tree_offset, threshold, default, feature = tree[offset]
        right_tree_offset = int(right_tree_offset)
        x = X[feature][inds]
        nans = np.isnan(x)
        
        inds0 = [
            np.less_equal(x, threshold),
            np.greater(x, threshold)
        ]

        inds0[0 if default == "left" else 1] |= nans
        offsets = [0, right_tree_offset]
        for i in range(2):
            predict_tree_inplace(tree, offset + 1 + offsets[i], X, y, inds[inds0[i]])
            
@cc.export(
    "predict_tree",
    numba.types.float64[::1](tree_type, list_of_arrays_type)
)
def predict_tree(tree, X):
    if not X:
        return np.zeros(0)
    X = numba.typed.List(X)
    y = np.ones(len(X[0]))
    predict_tree_inplace(tree, 0, X, y, np.arange(len(y)))
    return y

@cc.export(
    "midpoints_and_inds",
    numba.types.Tuple((list_of_arrays_type, list_of_ints_type))(list_of_arrays_type, numba.types.int64)
)
def midpoints_and_inds(X, max_bin):
    X_midpoints = numba.typed.List([np.array([1.])] * len(X))
    X_inds = numba.typed.List([np.array([1], np.uint8)] * len(X))
    
    for i in range(len(X)):
        x = X[i]
        sample = x[np.random.randint(0, len(x), 5000)]
        midpoints = np.nanpercentile(sample, np.linspace(0, 100, max_bin + 1)[1:-1])
        midpoints = midpoints[~np.isnan(midpoints)]
        midpoints = np.unique(midpoints)
        midpoints = np.hstack((midpoints, np.array([np.inf])))
        inds = np.digitize(x, midpoints)
        midpoints = np.hstack((midpoints, np.array([np.nan])))
        
        X_inds[i] = inds.astype(np.uint8)
        X_midpoints[i] = midpoints
        
    return X_midpoints, X_inds

# @cc.export(
#     "div_points",
#     numba.types.int64[::1](numba.types.i8, numba.types.i8)
# )
def div_points(Ntotal, Nsections):
    Neach_section, extras = divmod(Ntotal, Nsections)
    section_sizes = ([0] +
                     [Neach_section+1] * extras +
                     [Neach_section] * (Nsections-extras))
    div_points = np.cumsum(np.array(section_sizes, dtype=np.int64))
        
    return div_points

@cc.export(
    "_predict", 
    numba.types.float64[::1](trees_type, list_of_arrays_type)
)
def _predict(trees, X):
    # n = numba.get_num_threads()
    n = 8
    r = [np.array([1.])[:0]] * n
    points = div_points(len(trees), n)
    
    for i in range(n):
        st = points[i]
        end = points[i + 1]
        if st < end:
            a = predict_tree(trees[st], X)
            for t in trees[st + 1:end]:
                a *= predict_tree(t, X)
            r[i] = a
        
    res = np.ones(len(r[0]))
    points = div_points(len(r[0]), n)
    
    for i in range(n):
        st = points[i]
        end = points[i + 1]
        if st < end:
            for rr in r:
                if len(rr):
                    res[st:end] *= rr[st:end]
        
    return res

if __name__ == "__main__":
    cc.compile()
